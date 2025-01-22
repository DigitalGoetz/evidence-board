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



# def load_some_places(engine):
#     with Session(engine) as session:
#         country = Place(
#             name="United States",
#             type=PlaceType.COUNTRY,
#         )
#         state = Place(
#             name="New York",
#             type=PlaceType.STATE,
#         )
#         city = Place(
#             name="New York City",
#             type=PlaceType.CITY,
#         )

#         times_square = Location(
#             name="Times Square",
#             within=[country, state, city],
#         )

#         session.add_all([country, state, city, times_square])
#         session.commit()

# def find_times_square(engine):
#     with Session(engine) as session:
#         times_square = session.query(Location).filter(Location.name == "Times Square").first()
#         print(times_square.within[0].name)
#         print(times_square.within[1].name)
#         print(times_square.within[2].name)