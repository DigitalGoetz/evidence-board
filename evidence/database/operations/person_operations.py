from typing import List, Optional
from database.database_models import GroupDb, PersonDb, TagDb
from sqlalchemy.orm import Session, joinedload


class PersonDbOperations:
    def __init__(self, engine):
        self.engine = engine

    def create(self, person_name: str, affiliation_names: List[str]) -> Optional[PersonDb]:
        with Session(self.engine) as session:
            if self.exists(person_name):
                print(f"Person {person_name} already exists")
            else:
                affiliations = session.query(GroupDb).filter(GroupDb.name.in_(affiliation_names)).all()
                new_person = PersonDb(name=person_name, affiliations=affiliations, tags=[])

                session.add(new_person)
                session.commit()
                return new_person

        return None

    def delete(self, person_name: str) -> bool:
        with Session(self.engine) as session:
            try:
                # Find the person
                person = session.query(PersonDb).filter(PersonDb.name == person_name).first()
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

    def rename(self, person_name: str, new_name: str) -> Optional[PersonDb]:
        with Session(self.engine) as session:
            person = session.query(PersonDb).filter(PersonDb.name == person_name).first()
            if person:
                person.name = new_name
                session.commit()
                return person
            else:
                print(f"Person {person_name} not found")
                return None

    def tag(self, person_name: str, tag_name: str) -> Optional[PersonDb]:
        with Session(self.engine) as session:
            person = session.query(PersonDb).filter(PersonDb.name == person_name).first()
            tag = session.query(TagDb).filter(TagDb.name == tag_name).first()

            if person and tag:
                person.tags.append(tag)
                session.commit()
                return person

            return None

    def untag(self, person_name: str, tag_name: str) -> Optional[PersonDb]:
        with Session(self.engine) as session:
            person = session.query(PersonDb).filter(PersonDb.name == person_name).first()
            tag = session.query(TagDb).filter(TagDb.name == tag_name).first()

            if person and tag and tag.name in person.tags:
                person.tags.remove(tag)
                session.commit()
                return person

            return None

    def add_affiliation(self, person_name: str, affiliation_name: str) -> Optional[PersonDb]:
        with Session(self.engine) as session:
            person = session.query(PersonDb).filter(PersonDb.name == person_name).first()
            affiliation = session.query(GroupDb).filter(GroupDb.name == affiliation_name).first()

            if person and affiliation and affiliation not in person.affiliations:
                person.affiliations.append(affiliation)
                session.commit()
                return person

            return None

    def exists(self, person_name: str) -> bool:
        with Session(self.engine) as session:
            person_check = session.query(PersonDb).filter(PersonDb.name == person_name).first()

            if person_check:
                return True
            else:
                return False

    def get_all(self) -> List[PersonDb]:
        people = []
        with Session(self.engine) as session:
            found_people = session.query(PersonDb).options(joinedload(PersonDb.affiliations)).options(joinedload(PersonDb.tags)).all()
            for person in found_people:
                people.append(person)
        return people
