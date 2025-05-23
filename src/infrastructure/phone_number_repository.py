import sqlite3
from src.domain.phone_number import PhoneNumber
from src.domain.allocated_phone_number import AllocatedPhoneNumber
from src.domain.number_range import NumberRange
from src.domain.yearly_report import YearlyReport, YearlyRangeReport

class PhoneNumberAllocationError(Exception):
    """Exception levée lorsqu'aucun numéro ne peut être alloué."""
    pass

class PhoneNumberRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _get_number_range(self, range_id: int) -> NumberRange:
        conn = self._get_connection()
        cur = conn.cursor()
        cur.execute("SELECT start, end FROM number_range WHERE id = ?", (range_id,))
        row = cur.fetchone()
        conn.close()
        if row is None:
            raise ValueError(f"La plage de numéro avec l'id {range_id} n'existe pas.")
        return NumberRange(start=row["start"], end=row["end"])

    def _get_allocated_numbers(self, range_id: int) -> set:
        conn = self._get_connection()
        cur = conn.cursor()
        cur.execute("SELECT number FROM allocated_number WHERE range_id = ?", (range_id,))
        allocated = {row["number"] for row in cur.fetchall()}
        conn.close()
        return allocated

    def allocate_next_available(self, range_id: int, customer_id: int) -> PhoneNumber:
        """
        Expose à la couche métier une méthode d'allocation qui, en masquant le schéma DB,
        retourne le prochain numéro disponible.

        Les étapes internes sont :
          - Récupérer la plage complète via `_get_number_range`
          - Récupérer les numéros déjà alloués via `_get_allocated_numbers`
          - Calculer le premier numéro disponible dans la plage
          - Persister l'allocation dans la table `allocated_number`

        Retourne une instance de PhoneNumber représentant le numéro alloué.
        """
        number_range = self._get_number_range(range_id)
        allocated = self._get_allocated_numbers(range_id)

        next_available = None
        for num in range(number_range.start, number_range.end + 1):
            if num not in allocated:
                next_available = num
                break

        if next_available is None:
            raise PhoneNumberAllocationError("Aucun numéro disponible dans cette plage.")

        conn = self._get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO allocated_number (number, range_id, customer_id, allocated_at)
            VALUES (?, ?, ?, datetime('now'))
            """,
            (next_available, range_id, customer_id)
        )
        conn.commit()
        conn.close()

        # Retour de l'objet domaine PhoneNumber
        return AllocatedPhoneNumber(PhoneNumber(next_available), range_id, customer_id)

    def list_allocated_numbers(self, range_id: int) -> list:
        """
        Retourne la liste des numéros alloués dans la plage sous forme d'instances de PhoneNumber.
        """
        conn = self._get_connection()
        cur = conn.cursor()
        cur.execute("SELECT number, customer_id, range_id FROM allocated_number WHERE range_id = ? ORDER BY number ASC", (range_id,))
        rows = cur.fetchall()
        conn.close()
        return [AllocatedPhoneNumber(PhoneNumber(row["number"]), row["range_id"], row["customer_id"]) for row in rows]

    def list_ranges(self) -> list:
        """
        Retourne la liste des plages de numéros sous forme d'instances de NumberRange avec leur identifiant.
        """
        conn = self._get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, start, end FROM number_range")
        rows = cur.fetchall()
        conn.close()
        return [(row["id"], NumberRange(start=row["start"], end=row["end"])) for row in rows]

    def generate_yearly_usage_report(self, year: int) -> YearlyReport:
        """
        Génère un rapport pour l'année donnée.

        Retourne une liste de dictionnaires, chacun contenant pour une plage :
          - range_id
          - currently_allocated : nombre de numéros toujours actifs
          - new_allocated        : nombre de numéros alloués durant l'année
          - cancelled            : nombre de numéros annulés durant l'année
        """
        conn = self._get_connection()
        cur = conn.cursor()
        start_date = f"{year}-01-01"
        end_date   = f"{year}-12-31"
        query = """
        SELECT range_id,
               SUM(CASE WHEN cancelled_at IS NULL THEN 1 ELSE 0 END) AS currently_allocated,
               SUM(CASE WHEN allocated_at BETWEEN ? AND ? THEN 1 ELSE 0 END) AS new_allocated,
               SUM(CASE WHEN cancelled_at BETWEEN ? AND ? THEN 1 ELSE 0 END) AS cancelled
        FROM allocated_number
        GROUP BY range_id
        """
        cur.execute(query, (start_date, end_date, start_date, end_date))
        rows = cur.fetchall()
        conn.close()
        reports = [
            YearlyRangeReport(
                range_id=row["range_id"],
                currently_allocated=row["currently_allocated"],
                new_allocated=row["new_allocated"],
                cancelled=row["cancelled"]
            ) for row in rows
        ]
        return YearlyReport(range_reports=reports)

    def cancel_subscription(self, customer_id: int) -> None:
        """
        Marque la fin de l'abonnement d'un client en renseignant la date d'annulation.
        """
        conn = self._get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE allocated_number
            SET cancelled_at = datetime('now')
            WHERE customer_id = ? AND cancelled_at IS NULL
            """,
            (customer_id,)
        )
        conn.commit()
        conn.close()

    def release_expired_numbers(self) -> int:
        """
        Libère les numéros dont l'annulation remonte à plus de 6 mois.
        Ces numéros sont retirés de la table allocated_number, ce qui les
        rend à nouveau disponibles pour allocation.

        Retourne le nombre de numéros libérés.

        Pistes d'amélioration :
          - Garder les numeros annulés dans un cold storage
          - Garder les numeros annulés dans la db avec la possibilité de récupérer l'historique des customers
            Problématique: Changer la pk de la table allocated_number pour qu'elle soit composée de (customer_id, number)
        """
        conn = self._get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            DELETE FROM allocated_number
            WHERE cancelled_at IS NOT NULL
              AND cancelled_at <= date('now', '-6 months')
            """
        )
        released = cur.rowcount
        conn.commit()
        conn.close()
        return released
