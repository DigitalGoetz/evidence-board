from typing import List
from database.database_models import Group, GroupType, Person, Tag
from sqlalchemy.orm import Session


class TagOperations:
    def __init__(self):
        pass

    def create(self, engine, tag_name: str) -> bool:
        with Session(engine) as session:
            if self.exists(engine, tag_name):
                print(f"Tag {tag_name} already exists")
            else:
                new_tag = Tag(
                    name=tag_name,
                    groups=[],
                    people=[],
                    locations=[],
                )
                session.add(new_tag)
                session.commit()
                return True

        return False

    def exists(self, engine, tag_name: str) -> bool:
        with Session(engine) as session:
            tag_check = session.query(Tag).filter(Tag.name == tag_name).first()

            if tag_check:
                return True
            else:
                return False

    def get_all(self, engine):
        tags = []
        with Session(engine) as session:
            found_tags = session.query(Tag).all()
            for tag in found_tags:
                tags.append(tag)
        return tags

    def get_tagged(self, engine, tag_name: str):
        with Session(engine) as session:
            tag = session.query(Tag).filter(Tag.name == tag_name).first()
            if tag:
                return {
                    "groups": [group.name for group in tag.groups],
                    "people": [person.name for person in tag.people],
                    "locations": [location.name for location in tag.locations],
                }
            else:
                return {"groups": [], "people": [], "locations": []}

    def delete(self, engine, tag_name: str) -> bool:
        with Session(engine) as session:
            try:
                # Find the tag
                tag = session.query(Tag).filter(Tag.name == tag_name).first()
                if tag:
                    # Clear all references from objects that use this tag
                    for group in tag.groups:
                        group.tags.remove(tag)
                    for person in tag.people:
                        person.tags.remove(tag)
                    for location in tag.locations:
                        location.tags.remove(tag)

                    # Delete the tag itself
                    session.delete(tag)
                    session.commit()
                    return True
                else:
                    print(f"Tag {tag_name} not found")
                    return False
            except Exception as e:
                print(f"Error deleting tag: {e}")
                session.rollback()
                return False


class GroupOperations:
    def __init__(self):
        pass

    def rename(self, engine, group_name: str, new_name: str) -> bool:
        with Session(engine) as session:
            group = session.query(Group).filter(Group.name == group_name).first()
            if group:
                group.name = new_name
                session.commit()
                return True
            else:
                print(f"Group {group_name} not found")
                return False

    def delete(self, engine, group_name: str) -> bool:
        with Session(engine) as session:
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

    def create(self, engine, group_name: str, group_type: GroupType) -> bool:
        with Session(engine) as session:
            if self.exists(engine, group_name):
                print(f"Group {group_name} already exists")
            else:
                new_group = Group(
                    name=group_name,
                    type=group_type,
                    tags=[],
                )
                session.add(new_group)
                session.commit()
                return True

        return False

    def tag(self, engine, group_name: str, tag_name: str) -> bool:
        with Session(engine) as session:
            group = session.query(Group).filter(Group.name == group_name).first()
            tag = session.query(Tag).filter(Tag.name == tag_name).first()

            if group and tag:
                group.tags.append(tag)
                session.commit()
                return True

            return False

    def untag(self, engine, group_name: str, tag_name: str) -> bool:
        with Session(engine) as session:
            group = session.query(Group).filter(Group.name == group_name).first()
            tag = session.query(Tag).filter(Tag.name == tag_name).first()

            if group and tag and tag.name in group.tags:
                group.tags.remove(tag)
                session.commit()
                return True

            return False

    def exists(self, engine, group_name: str) -> bool:
        with Session(engine) as session:
            group_check = session.query(Group).filter(Group.name == group_name).first()

            if group_check:
                return True
            else:
                return False

    def get_all(self, engine):
        groups = []
        with Session(engine) as session:
            found_groups = session.query(Group).all()
            for group in found_groups:
                groups.append(group)
        return groups

    def remove_member(self, engine, group_name: str, person_name: str) -> bool:
        with Session(engine) as session:
            group = session.query(Group).filter(Group.name == group_name).first()
            person = session.query(Person).filter(Person.name == person_name).first()

            if group and person and person in group.members:
                group.members.remove(person)
                session.commit()
                return True

            return False


class PersonOperations:
    def __init__(self):
        pass

    def create(self, engine, person_name: str, affiliation_names: List[str]) -> bool:
        with Session(engine) as session:
            if self.exists(engine, person_name):
                print(f"Person {person_name} already exists")
            else:
                affiliations = (
                    session.query(Group).filter(Group.name.in_(affiliation_names)).all()
                )
                new_person = Person(
                    name=person_name, affiliations=affiliations, tags=[]
                )

                session.add(new_person)
                session.commit()
                return True

        return False

    def delete(self, engine, person_name: str) -> bool:
        with Session(engine) as session:
            try:
                # Find the person
                person = (
                    session.query(Person).filter(Person.name == person_name).first()
                )
                if person:
                    # Clear all references from objects that use this person
                    for affiliation in person.affiliations:
                        affiliation.members.remove(person)
                    for tag in person.tags:
                        tag.people.remove(person)

                    # Delete the person itself
                    session.delete(person)
                    session.commit()
                    return True
                else:
                    print(f"Person {person_name} not found")
                    return False
            except Exception as e:
                print(f"Error deleting person: {e}")
                session.rollback()
                return False

    def rename(self, engine, person_name: str, new_name: str) -> bool:
        with Session(engine) as session:
            person = session.query(Person).filter(Person.name == person_name).first()
            if person:
                person.name = new_name
                session.commit()
                return True
            else:
                print(f"Person {person_name} not found")
                return False

    def tag(self, engine, person_name: str, tag_name: str) -> bool:
        with Session(engine) as session:
            person = session.query(Person).filter(Person.name == person_name).first()
            tag = session.query(Tag).filter(Tag.name == tag_name).first()

            if person and tag:
                person.tags.append(tag)
                session.commit()
                return True

            return False

    def untag(self, engine, person_name: str, tag_name: str) -> bool:
        with Session(engine) as session:
            person = session.query(Person).filter(Person.name == person_name).first()
            tag = session.query(Tag).filter(Tag.name == tag_name).first()

            if person and tag and tag.name in person.tags:
                person.tags.remove(tag)
                session.commit()
                return True

            return False

    def add_affiliation(self, engine, person_name: str, affiliation_name: str) -> bool:
        with Session(engine) as session:
            person = session.query(Person).filter(Person.name == person_name).first()
            affiliation = (
                session.query(Group).filter(Group.name == affiliation_name).first()
            )

            if person and affiliation and affiliation not in person.affiliations:
                person.affiliations.append(affiliation)
                session.commit()
                return True

            return False

    def exists(self, engine, person_name: str) -> bool:
        with Session(engine) as session:
            person_check = (
                session.query(Person).filter(Person.name == person_name).first()
            )

            if person_check:
                return True
            else:
                return False

    def get_all(self, engine):
        people = []
        with Session(engine) as session:
            found_people = session.query(Group).all()
            for person in found_people:
                people.append(person)
        return person
