from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from database.database_models import TagDb
from database.database_exceptions import ObjectNotFoundException, ObjectInfoExistsException, ObjectInfoDoesNotExistException
from database.database_enumerations import OperationType, ObjectType


class BaseOperations(ABC):
    def __init__(self, engine, cls, object_type):
        self.engine = engine
        self.cls = cls
        self.object_type = object_type

    def _contains_tag(self, object, tag) -> bool:
        for object_tag in object.tags:
            if object_tag.name == tag.name:
                return True
        return False

    def rename(self, id: int, new_name: str):
        with Session(self.engine) as session:
            object = session.query(self.cls).filter(self.cls.id == id).first()

            if object:
                object.name = new_name
                session.commit()
                return self.get_by_id(object.id)
            else:
                session.rollback()
                raise ObjectNotFoundException(OperationType.RENAME, id, self.object_type)

    @abstractmethod
    def delete(self, id: int) -> None:
        pass

    def tag(self, id: int, tag_id: int):
        with Session(self.engine) as session:
            object = session.query(self.cls).filter(self.cls.id == id).first()
            tag = session.query(TagDb).filter(TagDb.id == tag_id).first()

            if object and tag and not self._contains_tag(object, tag):
                object.tags.append(tag)
                session.commit()
            else:
                if not object:
                    raise ObjectNotFoundException(OperationType.ADD_DETAIL, id, self.object_type)
                elif not tag:
                    raise ObjectNotFoundException(OperationType.ADD_DETAIL, tag_id, ObjectType.TAG)
                else:
                    raise ObjectInfoExistsException(id, self.object_type, tag_id)

            return self.get_by_id(object.id)

    def untag(self, id: int, tag_id: int):
        with Session(self.engine) as session:
            object = session.query(self.cls).filter(self.cls.id == id).first()
            tag = session.query(TagDb).filter(TagDb.id == tag_id).first()

            if object and tag and self._contains_tag(object, tag):
                object.tags.remove(tag)
                session.commit()
            else:
                if not object:
                    raise ObjectNotFoundException(OperationType.READ, id, self.object_type)
                elif not tag:
                    raise ObjectNotFoundException(OperationType.READ, tag_id, ObjectType.TAG)
                else:
                    raise ObjectInfoDoesNotExistException(id, self.object_type, tag_id)

            return self.get_by_id(object.id)

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, id):
        pass
