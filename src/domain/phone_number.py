from dataclasses import dataclass

@dataclass(frozen=True)
class PhoneNumber:
    number: int

    def formatted(self) -> str:
        """
        Retourne le numéro au format français classique : groupes de 2 chiffres, ex: "01 62 05 00 00".

        Pistes d'amélioration :
        - Ajout d'une localisation pour le séparateur des groupes de chiffres.
        - Plusieurs formats de numéros possibles (avec ou sans espaces, avec ou sans 0 devant le numéro...)
        """
        s = f"{self.number:010d}"
        return ' '.join(s[i:i+2] for i in range(0, 10, 2))

    def __str__(self):
        return self.formatted()
