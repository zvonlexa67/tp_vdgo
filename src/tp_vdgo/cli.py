import typer
from .config import Settings

from .kladr import loadDBF

from .db import dropdb as db_dropdb, createdb as create_db, dropusers as drop_users, createusers as create_users

app = typer.Typer(help="Управление списком задач")

@app.command()
def run():
    typer.echo("Запускаем основную программу")

@app.command()
def kladr():
    print("loadDBF()")
    loadDBF()
    

# @app.command()
# def kldr():
#     try:
#         k = kladr()
#         typer.echo(type(k))
#         typer.echo(k.loadDBF())
#     except RuntimeError as e:
#         typer.echo(f"Ошибка: {e}", err=True)
#         raise typer.Exit(code=1)
    
@app.command()
def createdb():
    try:
        createdb()
    except RuntimeError as e:
        typer.Exit(typer.echo(e, err=True))

@app.command()
def dropdb():
    try:
        db_dropdb()
    except RuntimeError as e:
        typer.Exit(typer.echo(e, err=True))

@app.command()
def dropusers():
    try:
        drop_users()
    except RuntimeError as e:
        typer.Exit(typer.echo(e, err=True))

@app.command()
def createusers():
    try:
        create_users()
    except RuntimeError as e:
        typer.Exit(typer.echo(e, err=True))

@app.command()
def createdb():
    try:
        create_db()
    except RuntimeError as e:
        typer.Exit(typer.echo(e, err=True))


if __name__ == "__main__":
    app()