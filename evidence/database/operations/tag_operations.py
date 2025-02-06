from typing import List
from sqlalchemy.orm import Session, joinedload
from database.database_models import TagDb
from database.database_exceptions import ObjectNotFoundException, ObjectAlreadyExistsException
from database.database_enumerations import OperationType, ObjectType


class TagDbOperations:
    def __init__(self, engine):
        self.engine = engine

    def rename(self, tag_id: int, new_name: str) -> TagDb:
        with Session(self.engine) as session:
            group = session.query(TagDb).filter(TagDb.id == tag_id).first()

            if group:
                group.name = new_name
                session.commit()
                return self.get_by_id(group.id)
            else:
                session.rollback()
                raise ObjectNotFoundException(OperationType.RENAME, tag_id, ObjectType.TAG)

    def delete(self, tag_id: int) -> None:
        with Session(self.engine) as session:
            tag = session.query(TagDb).filter(TagDb.id == tag_id).first()
            if tag:
                for group in tag.groups:
                    group.tags.remove(tag)
                for person in tag.people:
                    person.tags.remove(tag)
                for location in tag.locations:
                    location.tags.remove(tag)
                for place in tag.places:
                    place.tags.remove(tag)

                session.delete(tag)
                session.commit()
            else:
                raise ObjectNotFoundException(OperationType.DELETE, tag_id, ObjectType.TAG)

    def create(self, tag_name: str) -> TagDb:
        with Session(self.engine) as session:

            tag_check = session.query(TagDb).filter(TagDb.name == tag_name).first()

            if tag_check:
                raise ObjectAlreadyExistsException(tag_name, ObjectType.TAG)
            else:
                new_tag = TagDb(
                    name=tag_name,
                )
                session.add(new_tag)
                session.commit()
                return self.get_by_id(new_tag.id)

    def get_all(self) -> List[TagDb]:
        tags = []
        try:
            with Session(self.engine) as session:
                found_tags = (
                    session.query(TagDb)
                    .options(joinedload(TagDb.groups))
                    .options(joinedload(TagDb.people))
                    .options(joinedload(TagDb.locations))
                    .options(joinedload(TagDb.places))
                    .all()
                )
                for tag in found_tags:
                    tags.append(tag)
        except Exception as e:
            print(f"e: {e}")
        return tags

    def get_by_id(self, id) -> TagDb:
        with Session(self.engine) as session:

            tag = (
                session.query(TagDb)
                .filter(TagDb.id == id)
                .options(joinedload(TagDb.groups))
                .options(joinedload(TagDb.people))
                .options(joinedload(TagDb.locations))
                .options(joinedload(TagDb.places))
                .first()
            )
            if tag:
                return tag
            else:
                raise ObjectNotFoundException(OperationType.READ, id, ObjectType.TAG)
