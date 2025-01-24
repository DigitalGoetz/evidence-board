from typing import List, Optional
from database.database_models import Group, Person, Tag
from sqlalchemy.orm import Session, joinedload


class PersonOperations:
    def __init__(self, engine):
        self.engine = engine

    def create(self, person_name: str, affiliation_names: List[str]) -> Optional[Person]:
        with Session(self.engine) as session:
            if self.exists(person_name):
                print(f"Person {person_name} already exists")
            else:
                affiliations = session.query(Group).filter(Group.name.in_(affiliation_names)).all()
                new_person = Person(name=person_name, affiliations=affiliations, tags=[])

                session.add(new_person)
                session.commit()
                return new_person

        return None

    def delete(self, person_name: str) -> bool:
        with Session(self.engine) as session:
            try:
                # Find the person
                person = session.query(Person).filter(Person.name == person_name).first()
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

    def rename(self, person_name: str, new_name: str) -> Optional[Person]:
        with Session(self.engine) as session:
            person = session.query(Person).filter(Person.name == person_name).first()
            if person:
                person.name = new_name
                session.commit()
                return person
            else:
                print(f"Person {person_name} not found")
                return None

    def tag(self, person_name: str, tag_name: str) -> Optional[Person]:
        with Session(self.engine) as session:
            person = session.query(Person).filter(Person.name == person_name).first()
            tag = session.query(Tag).filter(Tag.name == tag_name).first()

            if person and tag:
                person.tags.append(tag)
                session.commit()
                return person

            return None

    def untag(self, person_name: str, tag_name: str) -> Optional[Person]:
        with Session(self.engine) as session:
            person = session.query(Person).filter(Person.name == person_name).first()
            tag = session.query(Tag).filter(Tag.name == tag_name).first()

            if person and tag and tag.name in person.tags:
                person.tags.remove(tag)
                session.commit()
                return person

            return None

    def add_affiliation(self, person_name: str, affiliation_name: str) -> Optional[Person]:
        with Session(self.engine) as session:
            person = session.query(Person).filter(Person.name == person_name).first()
            affiliation = session.query(Group).filter(Group.name == affiliation_name).first()

            if person and affiliation and affiliation not in person.affiliations:
                person.affiliations.append(affiliation)
                session.commit()
                return person

            return None

    def exists(self, person_name: str) -> bool:
        with Session(self.engine) as session:
            person_check = session.query(Person).filter(Person.name == person_name).first()

            if person_check:
                return True
            else:
                return False

    def get_all(self) -> List[Person]:
        people = []
        with Session(self.engine) as session:
            found_people = session.query(Person).options(joinedload(Person.affiliations)).options(joinedload(Person.tags)).all()
            for person in found_people:
                people.append(person)
        return people