from typing import List
from sqlalchemy.orm import Session, joinedload
from database.operations.base_operations import BaseOperations
from database.database_models import GroupDb, GroupType, PersonDb
from database.database_exceptions import ObjectNotFoundException, ObjectAlreadyExistsException, ObjectInfoExistsException, ObjectInfoDoesNotExistException
from database.database_enumerations import OperationType, ObjectType


class GroupDbOperations(BaseOperations):
    def __init__(self, engine):
        super().__init__(engine, GroupDb, ObjectType.GROUP)

    def _contains_person(self, group: GroupDb, person: PersonDb) -> bool:
        for group_member in group.members:
            if group_member.name == person.name:
                return True
        return False

    def delete(self, id: int) -> None:
        with Session(self.engine) as session:
            group = session.query(GroupDb).filter(GroupDb.id == id).first()
            if group:
                for person in group.members:
                    person.affiliations.remove(group)
                for tag in group.tags:
                    tag.groups.remove(group)

                session.delete(group)
                session.commit()
            else:
                raise ObjectNotFoundException(OperationType.DELETE, id, ObjectType.GROUP)

    def create(self, group_name: str, group_type: GroupType) -> GroupDb:
        with Session(self.engine) as session:

            group_check = session.query(GroupDb).filter(GroupDb.name == group_name).first()

            if group_check:
                raise ObjectAlreadyExistsException(group_name, ObjectType.GROUP)
            else:
                new_group = GroupDb(name=group_name, type=group_type)
                session.add(new_group)
                session.commit()
                return self.get_by_id(new_group.id)

    def get_all(self) -> List[GroupDb]:
        groups = []
        try:
            with Session(self.engine) as session:
                found_groups = session.query(GroupDb).options(joinedload(GroupDb.members)).options(joinedload(GroupDb.tags)).all()
                for group in found_groups:
                    groups.append(group)
        except Exception as e:
            print(f"e: {e}")
        return groups

    def get_by_id(self, id) -> GroupDb:
        with Session(self.engine) as session:
            group = session.query(GroupDb).filter(GroupDb.id == id).options(joinedload(GroupDb.members)).options(joinedload(GroupDb.tags)).first()
            if group:
                return group
            else:
                raise ObjectNotFoundException(OperationType.READ, id, ObjectType.GROUP)

    def remove_member(self, group_id: int, person_id: int) -> GroupDb:
        with Session(self.engine) as session:
            group = session.query(GroupDb).filter(GroupDb.id == group_id).first()
            person = session.query(PersonDb).filter(PersonDb.id == person_id).first()

            if group and person and self._contains_person(group, person):
                group.members.remove(person)
                session.commit()
            else:
                if not group:
                    raise ObjectNotFoundException(OperationType.REMOVE_DETAIL, group_id, ObjectType.GROUP)
                elif not person:
                    raise ObjectNotFoundException(OperationType.REMOVE_DETAIL, person_id, ObjectType.PERSON)
                else:
                    raise ObjectInfoDoesNotExistException(group_id, ObjectType.GROUP, person_id)

            return self.get_by_id(group.id)

    def add_member(self, group_id: int, person_id: int) -> GroupDb:
        with Session(self.engine) as session:
            group = session.query(GroupDb).filter(GroupDb.id == group_id).first()
            person = session.query(PersonDb).filter(PersonDb.id == person_id).first()

            if group and person and not self._contains_person(group, person):
                group.members.append(person)
                session.commit()
            else:
                if not group:
                    raise ObjectNotFoundException(OperationType.ADD_DETAIL, group_id, ObjectType.GROUP)
                elif not person:
                    raise ObjectNotFoundException(OperationType.ADD_DETAIL, person_id, ObjectType.PERSON)
                else:
                    raise ObjectInfoExistsException(group_id, ObjectType.GROUP, person_id)

            return self.get_by_id(group.id)
