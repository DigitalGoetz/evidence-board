from typing import List, Optional
from database.database_models import GroupDb, GroupType, PersonDb, TagDb
from sqlalchemy.orm import Session, joinedload


class GroupDbOperations:
    def __init__(self, engine):
        self.engine = engine

    def rename(self, group_name: str, new_name: str, eager: bool = False) -> Optional[GroupDb]:
        with Session(self.engine) as session:
            if eager:
                group = session.query(GroupDb).filter(GroupDb.name == group_name).options(joinedload(GroupDb.members)).options(joinedload(GroupDb.tags)).first()
            else:
                group = session.query(GroupDb).filter(GroupDb.name == group_name).first()

            if group:
                group.name = new_name
                session.commit()
                return group
            else:
                print(f"Group {group_name} not found")
                return None

    def delete(self, group_name: str) -> bool:
        with Session(self.engine) as session:
            try:
                # Find the group
                group = session.query(GroupDb).filter(GroupDb.name == group_name).first()
                if group:
                    # Clear all references from objects that use this group
                    for person in group.members:
                        person.affiliations.remove(group)
                    for tag in group.tags:
                        tag.groups.remove(group)

                    # Delete the group itself
                    session.delete(group)
                    session.commit()
                    return True
                else:
                    print(f"Group {group_name} not found")
                    return False
            except Exception as e:
                print(f"Error deleting group: {e}")
                session.rollback()
                return False

    def create(self, group_name: str, group_type: GroupType) -> Optional[GroupDb]:
        with Session(self.engine, expire_on_commit=False) as session:

            id = None

            if self._exists(group_name):
                print(f"Group {group_name} already exists")
            else:
                new_group = GroupDb(
                    name=group_name,
                    type=group_type,
                )
                session.add(new_group)
                session.commit()

                id = new_group.id

                return self.get_by_id(id)

        return session.query(GroupDb).filter(GroupDb.name == group_name).options(joinedload(GroupDb.members)).options(joinedload(GroupDb.tags)).first()

    def tag(self, group_name: str, tag_name: str) -> Optional[GroupDb]:
        with Session(self.engine) as session:
            group = session.query(GroupDb).filter(GroupDb.name == group_name).first()
            tag = session.query(TagDb).filter(TagDb.name == tag_name).first()

            if group and tag:
                # TODO check that tag doesn't already exist
                group.tags.append(tag)
                session.commit()
                return group

            return None

    def untag(self, group_name: str, tag_name: str) -> Optional[GroupDb]:
        with Session(self.engine) as session:
            group = session.query(GroupDb).filter(GroupDb.name == group_name).first()
            tag = session.query(TagDb).filter(TagDb.name == tag_name).first()

            if group and tag and tag.name in group.tags:
                group.tags.remove(tag)
                session.commit()
                return group

            return None

    def _exists(self, group_name: str) -> bool:
        with Session(self.engine) as session:
            group_check = session.query(GroupDb).filter(GroupDb.name == group_name).first()

            if group_check:
                return True
            else:
                return False

    def get_all(self) -> List[GroupDb]:
        groups = []
        with Session(self.engine) as session:
            found_groups = session.query(GroupDb).options(joinedload(GroupDb.members)).options(joinedload(GroupDb.tags)).all()
            for group in found_groups:
                groups.append(group)
        return groups

    def get_by_id(self, id) -> GroupDb:
        with Session(self.engine) as session:
            group = session.query(GroupDb).filter(GroupDb.id == id).options(joinedload(GroupDb.members)).options(joinedload(GroupDb.tags)).first()
            return group

    def get_by_name(self, group_name: str) -> GroupDb:
        with Session(self.engine) as session:
            group = session.query(GroupDb).filter(GroupDb.name == group_name).options(joinedload(GroupDb.members)).options(joinedload(GroupDb.tags)).first()
            return group

    def remove_member(self, group_name: str, person_name: str) -> Optional[GroupDb]:
        with Session(self.engine) as session:
            group = session.query(GroupDb).filter(GroupDb.name == group_name).first()
            person = session.query(PersonDb).filter(PersonDb.name == person_name).first()

            if group and person and person in group.members:
                group.members.remove(person)
                session.commit()

            return group
