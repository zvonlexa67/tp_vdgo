import typer

from .config import Settings
from .core.kladr import create as ck, drop as dk, truncate as tk, load as lk
from .core.db import dropdb as ddb, createdb as cdb, dropusers as ddu, createusers as cdu
from .core.auth import create as ca, drop as da

app = typer.Typer(help="Управление списком задач")

@app.command()
def run():
    typer.echo("Запускаем основную программу")

@app.command()
def kladr(create: bool = False, drop: bool = False, truncate: bool = False, load: bool = False):
    try:
        if truncate:
            tk()
        if drop:
            dk()
        if create:
            ck()
        if load:
            lk()
    except RuntimeError as e:
        typer.Exit(typer.echo(e, err=True))
    
@app.command()
def db(createusers: bool = False, createdb: bool = False, dropdb: bool = False, dropusers: bool = False):
    try:
        if createusers:
            cdu()
        if createdb:
            cdb()
        if dropdb:
            ddb()
        if dropusers:
            ddu()
    except RuntimeError as e:
        typer.Exit(typer.echo(e, err=True))

@app.command()
def auth(drop: bool = False, create: bool = False):
    try:
        if drop:
            da()
        if create:
            ca()
    except RuntimeError as e:
        typer.Exit(typer.echo(e, err=True))

if __name__ == "__main__":
    app()