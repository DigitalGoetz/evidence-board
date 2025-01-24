from typing import List, Optional
from database.database_models import Group, GroupType, Person, Tag
from sqlalchemy.orm import Session, joinedload

class GroupOperations:
    def __init__(self, engine):
        self.engine = engine

    def rename(self, group_name: str, new_name: str) -> Optional[Group]:
        with Session(self.engine) as session:
            group = session.query(Group).filter(Group.name == group_name).first()
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
                group = session.query(Group).filter(Group.name == group_name).first()
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

    def create(self, group_name: str, group_type: GroupType) -> Optional[Group]:
        with Session(self.engine) as session:
            if self.exists(group_name):
                print(f"Group {group_name} already exists")
            else:
                new_group = Group(
                    name=group_name,
                    type=group_type,
                    tags=[],
                )
                session.add(new_group)
                session.commit()
                return new_group

        return None

    def tag(self, group_name: str, tag_name: str) -> Optional[Group]:
        with Session(self.engine) as session:
            group = session.query(Group).filter(Group.name == group_name).first()
            tag = session.query(Tag).filter(Tag.name == tag_name).first()

            if group and tag:
                group.tags.append(tag)
                session.commit()
                return group

            return None

    def untag(self, group_name: str, tag_name: str) -> Optional[Group]:
        with Session(self.engine) as session:
            group = session.query(Group).filter(Group.name == group_name).first()
            tag = session.query(Tag).filter(Tag.name == tag_name).first()

            if group and tag and tag.name in group.tags:
                group.tags.remove(tag)
                session.commit()
                return group

            return None

    def exists(self, group_name: str) -> bool:
        with Session(self.engine) as session:
            group_check = session.query(Group).filter(Group.name == group_name).first()

            if group_check:
                return True
            else:
                return False

    def get_all(self) -> List[Group]:
        groups = []
        with Session(self.engine) as session:
            found_groups = session.query(Group).options(joinedload(Group.members)).options(joinedload(Group.tags)).all()
            for group in found_groups:
                groups.append(group)
        return groups
    
    def get_by_id(self, id) -> Group:
        with Session(self.engine) as session:
            group = session.query(Group).filter(Group.id == id).options(joinedload(Group.members)).options(joinedload(Group.tags)).first()
            return group
        
    def get_by_name(self, group_name: str) -> Group:
        with Session(self.engine) as session:
            group = session.query(Group).filter(Group.name == group_name).options(joinedload(Group.members)).options(joinedload(Group.tags)).first()
            return group

    def remove_member(self, group_name: str, person_name: str) -> Optional[Group]:
        with Session(self.engine) as session:
            group = session.query(Group).filter(Group.name == group_name).first()
            person = session.query(Person).filter(Person.name == person_name).first()

            if group and person and person in group.members:
                group.members.remove(person)
                session.commit()
                return group

            return None