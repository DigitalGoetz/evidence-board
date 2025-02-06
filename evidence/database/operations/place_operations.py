from typing import List
from database.operations.base_operations import BaseOperations
from database.database_models import PlaceDb, LocationDb
from sqlalchemy.orm import Session, joinedload
from database.database_exceptions import ObjectNotFoundException, ObjectAlreadyExistsException, ObjectInfoExistsException, ObjectInfoDoesNotExistException
from database.database_enumerations import OperationType, ObjectType


class PlaceDbOperations(BaseOperations):

    def __init__(self, engine):
        super().__init__(engine, PlaceDb, ObjectType.PLACE)

    def _is_within(self, place: PlaceDb, location: LocationDb) -> bool:
        for within_locations in place.within:
            if within_locations.name == location.name:
                return True
        return False

    def delete(self, id: int) -> None:
        with Session(self.engine) as session:
            place = session.query(PlaceDb).filter(PlaceDb.id == id).first()

            if place:
                for within_location in place.within:
                    within_location.contains.remove(place)
                for tag in place.tags:
                    tag.people.remove(place)

                session.delete(place)
                session.commit()
            else:
                raise ObjectNotFoundException(OperationType.DELETE, id, ObjectType.PLACE)

    def create(self, place_name: str) -> PlaceDb:
        with Session(self.engine) as session:

            place_check = session.query(PlaceDb).filter(PlaceDb.name == place_name).first()

            if place_check:
                raise ObjectAlreadyExistsException(place_name, ObjectType.PLACE)
            else:
                new_place = PlaceDb(name=place_name)

                session.add(new_place)
                session.commit()
                return self.get_by_id(new_place.id)

    def set_within(self, place_id: int, location_id: int) -> PlaceDb:

        with Session(self.engine) as session:
            place = session.query(PlaceDb).filter(PlaceDb.id == place_id).first()
            location = session.query(LocationDb).filter(LocationDb.id == location_id).first()

            if place and location and not self._is_within(place, location):
                place.within.append(location)
                session.commit()
            else:
                if not location:
                    raise ObjectNotFoundException(OperationType.ADD_DETAIL, location_id, ObjectType.LOCATION)
                elif not place:
                    raise ObjectNotFoundException(OperationType.ADD_DETAIL, place_id, ObjectType.PLACE)
                else:
                    raise ObjectInfoExistsException(place_id, ObjectType.PLACE, location_id)

            return self.get_by_id(place.id)

    def unset_within(self, place_id: int, location_id: int) -> PlaceDb:
        with Session(self.engine) as session:
            location = session.query(LocationDb).filter(LocationDb.id == location_id).first()
            place = session.query(PlaceDb).filter(PlaceDb.id == place_id).first()

            if location and place and self._is_within(place, location):
                place.within.remove(place)
                session.commit()
            else:
                if not location:
                    raise ObjectNotFoundException(OperationType.REMOVE_DETAIL, location_id, ObjectType.LOCATION)
                elif not place:
                    raise ObjectNotFoundException(OperationType.REMOVE_DETAIL, place_id, ObjectType.PLACE)
                else:
                    raise ObjectInfoDoesNotExistException(place_id, ObjectType.PLACE, location_id)

            return self.get_by_id(place.id)

    def get_all(self) -> List[PlaceDb]:
        places = []
        try:
            with Session(self.engine) as session:
                found_places = session.query(PlaceDb).options(joinedload(PlaceDb.within)).options(joinedload(PlaceDb.tags)).all()
                for place in found_places:
                    places.append(place)
        except Exception as e:
            print(f"e: {e}")
        return places

    def get_by_id(self, id) -> PlaceDb:
        with Session(self.engine) as session:
            place = session.query(PlaceDb).filter(PlaceDb.id == id).options(joinedload(PlaceDb.within)).options(joinedload(PlaceDb.tags)).first()
            if place:
                return place
            else:
                raise ObjectNotFoundException(OperationType.READ, id, ObjectType.PLACE)
