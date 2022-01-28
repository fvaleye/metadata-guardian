import typer

app = typer.Typer()

from . import external, local

app.add_typer(external.app, name="external-sources")
app.add_typer(local.app, name="local-sources")


def main() -> None:
    app()
