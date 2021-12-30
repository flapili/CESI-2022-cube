# coding: utf-8
import zoneinfo
import datetime
from typing import List

import typer
from sqlmodel import Session, create_engine, select

import db
from utils import hash_password
from settings import get_settings

s = get_settings()

app = typer.Typer()
psql_url = f"postgresql://{s.postgres_user}:{s.postgres_password.get_secret_value()}@{s.postgres_host}:{s.postgres_port}/{s.postgres_database}"  # noqa

engine = create_engine(psql_url)

user_app = typer.Typer(name="user")
app.add_typer(user_app)


@user_app.command(name="list")
def user_list():
    """Liste tous les utilisateurs."""
    query = select(db.User)
    with Session(engine) as session:
        users: List[db.User] = session.execute(query)
        for user in users:
            user: db.User = dict(user)["User"]
            typer.echo(user.json())


@user_app.command(name="create")
def user_create(
    firstname: str = typer.Option(..., prompt=True),
    lastname: str = typer.Option(..., prompt=True),
    email: str = typer.Option(..., prompt=True),
    phone_number: str = typer.Option(..., prompt=True),
    birthday: datetime.datetime = typer.Option(..., prompt=True),
    password: str = typer.Option(..., prompt=True, confirmation_prompt=True, hide_input=True),
    user_type: db.UserType = typer.Option(..., prompt=True),
):
    """Crée un utilisateur."""
    user = db.User(
        firstname=firstname,
        lastname=lastname,
        email=email,
        phone_number=phone_number,
        birthday=birthday,
        hashed_password=hash_password(password),
        type=user_type,
    )
    with Session(engine) as session:
        session.add(user)
        session.commit()
    typer.secho(f"added user '{firstname} {lastname}'", fg="green")


@user_app.command("fake")
def user_fake(
    n: int = typer.Argument(..., help="Nombre d'utilisateur à générer"),
):
    if n < 1:
        typer.secho("n must be greater than 0", fg="red")
        typer.Exit(1)

    import random
    import faker

    fake = faker.Faker(locale="fr-FR")

    with Session(engine) as session:
        for _ in range(n):
            firstname = fake.first_name()
            lastname = fake.last_name()
            session.add(
                db.User(
                    firstname=firstname,
                    lastname=lastname,
                    email=f"contact.flapili+fake{firstname}{lastname}@gmail.com",
                    phone_number=f"06 {random.randint(0, 99):02} {random.randint(0, 99):02} {random.randint(0, 99):02} {random.randint(0, 99):02}",  # noqa
                    hashed_password=hash_password("fake"),
                    birthday=datetime.datetime.combine(
                        fake.date_of_birth(tzinfo=zoneinfo.ZoneInfo("UTC"), minimum_age=13, maximum_age=70),
                        datetime.datetime.min.time(),
                    ),
                )
            )

        session.commit()
    typer.secho(f"added {n} fake user", fg="green")


if __name__ == "__main__":
    app()
