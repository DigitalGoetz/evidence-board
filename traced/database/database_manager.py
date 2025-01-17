from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from database.database_models import Base, Group, GroupType, Person


def get_engine():
    # Format: postgresql://username:password@host:port/database_name
    username = "evidence"
    password = "evidence"
    host = "localhost"
    port = "5432"
    database = "evidence"
    
    database_url = f"postgresql://{username}:{password}@{host}:{port}/{database}"

    engine = create_engine(database_url, echo=True)
    Base.metadata.create_all(engine)
    return engine

def load_some_people(engine):
    with Session(engine) as session:
        elks = Group(
            name="elk lodge",
            type=GroupType.ORGANIZATION,
        )
        chess_club = Group(
            name="chess club",
            type=GroupType.ORGANIZATION,
        )

        # Create people
        spongebob = Person(
            name="spongebob",
            affiliations=[elks, chess_club]  # Can be in multiple groups
        )
        patrick = Person(
            name="patrick",
            affiliations=[elks]  # Can be in one group
        )

        session.add_all([elks, chess_club, spongebob, patrick])
        session.commit()