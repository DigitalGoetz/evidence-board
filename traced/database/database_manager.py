from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from database.database_models import Base, Group, GroupType, Person, Place, PlaceType, Location


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


