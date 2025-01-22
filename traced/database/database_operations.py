
from typing import List
from database.database_models import Group, GroupType, Person
from sqlalchemy.orm import Session

class GroupOperations:
    def __init__(self):
        pass

    def create(self, engine, group_name: str, group_type: GroupType) -> bool:
        with Session(engine) as session:
            if self.exists(engine, group_name):
                print(f"Group {group_name} already exists")
            else:
                new_group = Group(
                    name=group_name,
                    type=group_type,
                )
                session.add(new_group)
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
    
class PersonOperations:
    def __init__(self):
        pass

    def create(self, engine, person_name: str, affiliation_names: List[str]) -> bool:
        with Session(engine) as session:
            if self.exists(engine, person_name):
                print(f"Person {person_name} already exists")
            else:
                affiliations = session.query(Group).filter(Group.name.in_(affiliation_names)).all()
                new_person = Person(
                    name=person_name,
                    affiliations=affiliations,
                )
                
                session.add(new_person)
                session.commit()
                return True
        
        return False

    def exists(self, engine, person_name: str) -> bool:
        with Session(engine) as session:
            person_check = session.query(Person).filter(Person.name == person_name).first()

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
            

def load_some_people(engine):
    with Session(engine) as session:
        elks = Group(
            name="elk lodge",
            type=GroupType.ORGANIZATION,
        )
        chess_club = Group(
            name="chess club",
            type=GroupType.ORGANIZATION,
        )

        # Create people
        spongebob = Person(
            name="spongebob",
            affiliations=[elks, chess_club]  # Can be in multiple groups
        )
        patrick = Person(
            name="patrick",
            affiliations=[elks]  # Can be in one group
        )

        session.add_all([elks, chess_club, spongebob, patrick])
        session.commit()