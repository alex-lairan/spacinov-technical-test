import click

@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = "foo"

@cli.command()
@click.option("--customer-id", required=True)
@click.pass_context
def allocate(ctx, customer_id):
    click.echo(f"test = {ctx.obj} customer-id = {customer_id}")

@cli.command()
@click.pass_context
def list_allocated(ctx):
    click.echo("allocated numbers")
