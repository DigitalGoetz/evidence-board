from typing import List
from database.operations.base_operations import BaseOperations
from database.database_models import LocationDb, LocationType, PlaceDb
from database.database_exceptions import ObjectNotFoundException, ObjectAlreadyExistsException, ObjectInfoExistsException, ObjectInfoDoesNotExistException
from database.database_enumerations import OperationType, ObjectType
from sqlalchemy.orm import Session, joinedload


class LocationDbOperations(BaseOperations):

    def __init__(self, engine):
        super().__init__(engine, LocationDb, ObjectType.LOCATION)

    def _contains_place(self, location: LocationDb, place: PlaceDb) -> bool:
        for contained_places in location.contains:
            if contained_places.name == place.name:
                return True
        return False

    def delete(self, id: int) -> None:
        with Session(self.engine) as session:
            location = session.query(LocationDb).filter(LocationDb.id == id).first()
            if location:
                for place in location.contains:
                    place.within.remove(location)
                for tag in location.tags:
                    tag.locations.remove(location)

                session.delete(location)
                session.commit()
            else:
                raise ObjectNotFoundException(OperationType.DELETE, id, ObjectType.GROUP)

    def create(self, location_name: str, location_type: LocationType) -> LocationDb:
        with Session(self.engine) as session:

            location_check = session.query(LocationDb).filter(LocationDb.name == location_name).first()

            if location_check:
                raise ObjectAlreadyExistsException(location_name, ObjectType.LOCATION)
            else:
                new_location = LocationDb(name=location_name, type=location_type)
                session.add(new_location)
                session.commit()
                return self.get_by_id(new_location.id)

    def get_all(self) -> List[LocationDb]:
        locations = []
        try:
            with Session(self.engine) as session:
                found_locations = session.query(LocationDb).options(joinedload(LocationDb.contains)).options(joinedload(LocationDb.tags)).all()
                for location in found_locations:
                    locations.append(location)
        except Exception as e:
            print(f"e: {e}")
        return locations

    def get_by_id(self, id) -> LocationDb:
        with Session(self.engine) as session:
            location = session.query(LocationDb).filter(LocationDb.id == id).options(joinedload(LocationDb.contains)).options(joinedload(LocationDb.tags)).first()
            if location:
                return location
            else:
                raise ObjectNotFoundException(OperationType.READ, id, ObjectType.LOCATION)

    def remove_place(self, location_id: int, place_id: int) -> LocationDb:
        with Session(self.engine) as session:
            location = session.query(LocationDb).filter(LocationDb.id == location_id).first()
            place = session.query(PlaceDb).filter(PlaceDb.id == place_id).first()

            if location and place and self._contains_place(location, place):
                location.contains.remove(place)
                session.commit()
            else:
                if not location:
                    raise ObjectNotFoundException(OperationType.REMOVE_DETAIL, location_id, ObjectType.LOCATION)
                elif not place:
                    raise ObjectNotFoundException(OperationType.REMOVE_DETAIL, place_id, ObjectType.PLACE)
                else:
                    raise ObjectInfoDoesNotExistException(location_id, ObjectType.LOCATION, place_id)

            return self.get_by_id(location.id)

    def add_place(self, location_id: int, place_id: int) -> LocationDb:
        with Session(self.engine) as session:
            location = session.query(LocationDb).filter(LocationDb.id == location_id).first()
            place = session.query(PlaceDb).filter(PlaceDb.id == place_id).first()

            if location and place and not self._contains_place(location, place):
                location.contains.append(place)
                session.commit()
            else:
                if not location:
                    raise ObjectNotFoundException(OperationType.ADD_DETAIL, location_id, ObjectType.LOCATION)
                elif not place:
                    raise ObjectNotFoundException(OperationType.ADD_DETAIL, place_id, ObjectType.PLACE)
                else:
                    raise ObjectInfoExistsException(location_id, ObjectType.LOCATION, place_id)

            return self.get_by_id(location.id)
