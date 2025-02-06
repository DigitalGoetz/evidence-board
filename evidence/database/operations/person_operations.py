from typing import List
from database.operations.base_operations import BaseOperations
from database.database_models import GroupDb, PersonDb
from sqlalchemy.orm import Session, joinedload
from database.database_exceptions import ObjectNotFoundException, ObjectAlreadyExistsException, ObjectInfoExistsException, ObjectInfoDoesNotExistException
from database.database_enumerations import OperationType, ObjectType


class PersonDbOperations(BaseOperations):
    def __init__(self, engine):
        super().__init__(engine, PersonDb, ObjectType.PERSON)

    def _is_affiliated(self, person: PersonDb, group: GroupDb) -> bool:
        for affiliation in person.affiliations:
            if affiliation.name == group.name:
                return True
        return False

    def delete(self, id: int) -> None:
        with Session(self.engine) as session:
            person = session.query(PersonDb).filter(PersonDb.id == id).first()

            if person:
                for affiliation in person.affiliations:
                    affiliation.members.remove(person)
                for tag in person.tags:
                    tag.people.remove(person)

                session.delete(person)
                session.commit()
            else:
                raise ObjectNotFoundException(OperationType.DELETE, id, ObjectType.PERSON)

    def create(self, person_name: str) -> PersonDb:
        with Session(self.engine) as session:

            person_check = session.query(PersonDb).filter(PersonDb.name == person_name).first()

            if person_check:
                raise ObjectAlreadyExistsException(person_name, ObjectType.PERSON)
            else:
                new_person = PersonDb(name=person_name)

                session.add(new_person)
                session.commit()
                return self.get_by_id(new_person.id)

    def add_affiliation(self, person_id: int, affiliation_id: int) -> PersonDb:

        with Session(self.engine) as session:
            person = session.query(PersonDb).filter(PersonDb.id == person_id).first()
            affiliation = session.query(GroupDb).filter(GroupDb.id == affiliation_id).first()

            if person and affiliation and not self._is_affiliated(person, affiliation):
                person.affiliations.append(affiliation)
                session.commit()
            else:
                if not affiliation:
                    raise ObjectNotFoundException(OperationType.ADD_DETAIL, affiliation_id, ObjectType.GROUP)
                elif not person:
                    raise ObjectNotFoundException(OperationType.ADD_DETAIL, person_id, ObjectType.PERSON)
                else:
                    raise ObjectInfoExistsException(person_id, ObjectType.PERSON, affiliation_id)

            return self.get_by_id(person.id)

    def remove_affiliation(self, person_id: int, affiliation_id: int) -> PersonDb:
        with Session(self.engine) as session:
            group = session.query(GroupDb).filter(GroupDb.id == affiliation_id).first()
            person = session.query(PersonDb).filter(PersonDb.id == person_id).first()

            if group and person and self._is_affiliated(person, group):
                person.affiliations.remove(person)
                session.commit()
            else:
                if not group:
                    raise ObjectNotFoundException(OperationType.REMOVE_DETAIL, affiliation_id, ObjectType.GROUP)
                elif not person:
                    raise ObjectNotFoundException(OperationType.REMOVE_DETAIL, person_id, ObjectType.PERSON)
                else:
                    raise ObjectInfoDoesNotExistException(person_id, ObjectType.PERSON, affiliation_id)

            return self.get_by_id(person.id)

    def get_all(self) -> List[PersonDb]:
        people = []
        try:
            with Session(self.engine) as session:
                found_people = session.query(PersonDb).options(joinedload(PersonDb.affiliations)).options(joinedload(PersonDb.tags)).all()
                for person in found_people:
                    people.append(person)
        except Exception as e:
            print(f"e: {e}")
        return people

    def get_by_id(self, id) -> PersonDb:
        with Session(self.engine) as session:
            person = session.query(PersonDb).filter(PersonDb.id == id).options(joinedload(PersonDb.affiliations)).options(joinedload(PersonDb.tags)).first()
            if person:
                return person
            else:
                raise ObjectNotFoundException(OperationType.READ, id, ObjectType.PERSON)
