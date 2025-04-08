import click
from src.infrastructure.phone_number_repository import PhoneNumberRepository, PhoneNumberAllocationError

@click.group()
@click.pass_context
def cli(ctx):
    # TODO: Utiliser un .env pour configurer le chemin vers la base de données
    db_path = "data/phone_alloc.db"
    ctx.obj = {"repository": PhoneNumberRepository(db_path)}

@cli.command()
@click.option("--customer-id", required=True, type=int, help="Identifiant du client")
@click.option("--range-id", default=1, type=int, show_default=True, help="Identifiant de la plage (par défaut 1)")
@click.pass_context
def allocate(ctx, customer_id, range_id):
    """
    Alloue le prochain numéro disponible pour la plage spécifiée.
    """
    repository = ctx.obj["repository"]
    try:
        phone = repository.allocate_next_available(range_id, customer_id)
        click.echo(f"Numéro alloué: {phone}")
    except PhoneNumberAllocationError as e:
        click.echo(f"Erreur lors de l'allocation: {e}")
    except Exception as e:
        click.echo(f"Erreur inconnue: {e}")

@cli.command()
@click.option("--range-id", default=1, type=int, show_default=True, help="Identifiant de la plage (par défaut 1)")
@click.pass_context
def list_allocated(ctx, range_id):
    """
    Affiche la liste des numéros alloués pour la plage spécifiée.
    """
    repository = ctx.obj["repository"]
    allocated_numbers = repository.list_allocated_numbers(range_id)
    if allocated_numbers:
        click.echo("Numéros alloués:")
        for phone in allocated_numbers:
            click.echo(f" - {phone}")
    else:
        click.echo("Aucun numéro alloué dans cette plage.")

@cli.command()
@click.pass_context
def list_ranges(ctx):
    """
    Affiche la liste des plages de numéros existantes avec leur identifiant.
    """
    repository = ctx.obj["repository"]
    ranges = repository.list_ranges()
    if ranges:
        click.echo("Plages de numéros existantes :")
        for range_id, num_range in ranges:
            start_str = " ".join(f"{num_range.start:010d}"[i:i+2] for i in range(0, 10, 2))
            end_str = " ".join(f"{num_range.end:010d}"[i:i+2] for i in range(0, 10, 2))
            click.echo(f"ID {range_id} : {start_str} à {end_str}")
    else:
        click.echo("Aucune plage de numéros n'existe.")

@cli.command()
@click.option("--year", required=True, type=int, help="Année pour le rapport")
@click.pass_context
def usage_report(ctx, year):
    """
    Génère un rapport annuel indiquant pour chaque plage :
      - Le nombre de numéros actuellement alloués.
      - Le nombre de numéros nouvellement alloués durant l'année.
      - Le nombre de numéros annulés durant l'année.
    """
    repository = ctx.obj["repository"]
    try:
        report = repository.generate_yearly_usage_report(year)
        if report.range_reports:
            click.echo(f"Rapport d'utilisation pour l'année {year} :")
            for r in report.range_reports:
                click.echo(
                    f"Plage ID {r.range_id} : {r.currently_allocated} alloués, " +
                    f"{r.new_allocated} nouvellement alloués, {r.cancelled} annulés."
                )
        else:
            click.echo("Aucun enregistrement trouvé pour l'année donnée.")
    except Exception as e:
        click.echo(f"Erreur lors de la génération du rapport : {e}")


if __name__ == "__main__":
    cli()
