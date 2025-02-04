from typing import List, Optional
from database.database_models import TagDb, LocationDb, PlaceDb
from sqlalchemy.orm import Session, joinedload


class PlaceDbOperations:

    def __init__(self, engine):
        self.engine = engine

    def create(self, place_name: str, within_name: str) -> Optional[PlaceDb]:
        with Session(self.engine) as session:
            if self.exists(place_name):
                print(f"Place {place_name} already exists")
            else:
                within = session.query(LocationDb).filter(LocationDb.name == within_name).first()
                new_place = PlaceDb(name=place_name, within=within)

                session.add(new_place)
                session.commit()
                return new_place
        return None

    def delete(self, place_name: str) -> bool:
        with Session(self.engine) as session:
            try:
                # Find the Place
                place = session.query(PlaceDb).filter(PlaceDb.name == place_name).first()
                if place:
                    # Clear all references from objects that use this Place
                    for location in place.within:
                        location.contains.remove(place)

                    # Delete the place itself
                    session.delete(place)
                    session.commit()
                    return True
                else:
                    print(f"Place {place_name} not found")
                    return False
            except Exception as e:
                print(f"Error deleting place: {e}")
                session.rollback()
                return False

    def rename(self, place_name: str, new_name: str) -> Optional[PlaceDb]:
        with Session(self.engine) as session:
            place = session.query(PlaceDb).filter(PlaceDb.name == place_name).first()
            if place:
                place.name = new_name
                session.commit()
                return place
            else:
                print(f"Place {place_name} not found")
                return None

    def tag(self, place_name: str, tag_name: str) -> Optional[PlaceDb]:
        with Session(self.engine) as session:
            place = session.query(PlaceDb).filter(PlaceDb.name == place_name).first()
            tag = session.query(TagDb).filter(TagDb.name == tag_name).first()

            if place and tag:
                place.tags.append(tag)
                session.commit()
                return place

            return None

    def untag(self, place_name: str, tag_name: str) -> Optional[PlaceDb]:
        with Session(self.engine) as session:
            place = session.query(PlaceDb).filter(PlaceDb.name == place_name).first()
            tag = session.query(TagDb).filter(TagDb.name == tag_name).first()

            if place and tag and tag.name in place.tags:
                place.tags.remove(tag)
                session.commit()
                return place

            return None

    def exists(self, place_name: str) -> bool:
        with Session(self.engine) as session:
            place_check = session.query(PlaceDb).filter(PlaceDb.name == place_name).first()

            if place_check:
                return True
            else:
                return False

    def get_all(self) -> List[PlaceDb]:
        places = []
        with Session(self.engine) as session:
            found_places = session.query(PlaceDb).options(joinedload(PlaceDb.within)).options(joinedload(PlaceDb.tags)).all()
            for place in found_places:
                places.append(place)
        return places

    def located_within(self, place_name: str, within_location: str) -> Optional[PlaceDb]:
        with Session(self.engine) as session:
            place = session.query(PlaceDb).filter(PlaceDb.name == place_name).first()
            containing_location = session.query(LocationDb).filter(LocationDb.name == within_location).first()

            if place and containing_location and place not in containing_location.contains and containing_location not in place.within:
                place.within.append(containing_location)
                session.commit()
                return place

            return None
