from typing import List, Optional
from database.database_models import TagDb, LocationDb, LocationType
from sqlalchemy.orm import Session, joinedload


class LocationDbOperations:

    def __init__(self, engine):
        self.engine = engine

    def create(self, location_name: str, location_type: LocationType) -> Optional[LocationDb]:
        with Session(self.engine) as session:
            if self.exists(location_name):
                print(f"Location {location_name} already exists")
            else:
                new_place = LocationDb(name=location_name, type=location_type)

                session.add(new_place)
                session.commit()
                return new_place
        return None

    def delete(self, location_name: str) -> bool:
        with Session(self.engine) as session:
            try:
                # Find the Location
                location = session.query(LocationDb).filter(LocationDb.name == location_name).first()
                if location:
                    # Clear all references from objects that use this Location
                    for place in location.contains:
                        place.within.remove(place)

                    # Delete the place itself
                    session.delete(place)
                    session.commit()
                    return True
                else:
                    print(f"Location {location_name} not found")
                    return False
            except Exception as e:
                print(f"Error deleting location: {e}")
                session.rollback()
                return False

    def rename(self, location_name: str, new_name: str) -> Optional[LocationDb]:
        with Session(self.engine) as session:
            location = session.query(LocationDb).filter(LocationDb.name == location_name).first()
            if location:
                location.name = new_name
                session.commit()
                return location
            else:
                print(f"Location {location_name} not found")
                return None

    def tag(self, location_name: str, tag_name: str) -> Optional[LocationDb]:
        with Session(self.engine) as session:
            location = session.query(LocationDb).filter(LocationDb.name == location_name).first()
            tag = session.query(TagDb).filter(TagDb.name == tag_name).first()

            if location and tag:
                location.tags.append(tag)
                session.commit()
                return location

            return None

    def untag(self, location_name: str, tag_name: str) -> Optional[LocationDb]:
        with Session(self.engine) as session:
            location = session.query(LocationDb).filter(LocationDb.name == location_name).first()
            tag = session.query(TagDb).filter(TagDb.name == tag_name).first()

            if location and tag and tag.name in location.tags:
                location.tags.remove(tag)
                session.commit()
                return location

            return None

    def exists(self, location_name: str) -> bool:
        with Session(self.engine) as session:
            location_check = session.query(LocationDb).filter(LocationDb.name == location_name).first()

            if location_check:
                return True
            else:
                return False

    def get_all(self) -> List[LocationDb]:
        locations = []
        with Session(self.engine) as session:
            found_locations = session.query(LocationDb).options(joinedload(LocationDb.contains)).options(joinedload(LocationDb.tags)).all()
            for location in found_locations:
                locations.append(location)
        return locations
