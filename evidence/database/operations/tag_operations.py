from typing import List, Dict, Optional
from database.database_models import Tag
from sqlalchemy.orm import Session


class TagOperations:
    def __init__(self, engine):
        self.engine = engine

    def create(self, name: str) -> Optional[Tag]:
        with Session(self.engine, expire_on_commit=False) as session:
            if self.exists(name):
                print(f"Tag {name} already exists")
                return self.get_by_name(name)
            else:
                new_tag = Tag(
                    name=name,
                    groups=[],
                    people=[],
                    locations=[],
                )
                print("first")
                print(new_tag)
                session.add(new_tag)
                session.commit()
                print("second  ")
                print(new_tag)
                return new_tag

        return None

    def exists(self, tag_name: str) -> bool:
        with Session(self.engine) as session:
            tag_check = session.query(Tag).filter(Tag.name == tag_name).first()

            if tag_check:
                return True
            else:
                return False

    def get_all(self) -> List[Tag]:
        tags = []
        with Session(self.engine) as session:
            found_tags = session.query(Tag).all()
            for tag in found_tags:
                tags.append(tag)
        return tags

    def get_tagged(self, tag_name: str) -> Dict:
        with Session(self.engine) as session:
            tag = session.query(Tag).filter(Tag.name == tag_name).first()
            if tag:
                return {
                    "groups": [group.name for group in tag.groups],
                    "people": [person.name for person in tag.people],
                    "locations": [location.name for location in tag.locations],
                }
            else:
                return {"groups": [], "people": [], "locations": []}

    def get_by_id(self, tag_name: str) -> Tag:
        with Session(self.engine) as session:
            tag = session.query(Tag).filter(Tag.name == tag_name).first()
            return tag

    def get_by_name(self, tag_name: str) -> Tag:
        with Session(self.engine) as session:
            tag = session.query(Tag).filter(Tag.name == tag_name).first()
            return tag

    def delete(self, tag_name: str) -> bool:
        with Session(self.engine) as session:
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
