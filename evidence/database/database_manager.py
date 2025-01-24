from sqlalchemy import create_engine

from database.operations.group_operations import GroupOperations
from database.operations.person_operations import PersonOperations
from database.operations.place_operations import PlaceOperations
from database.operations.location_operations import LocationOperations
from database.operations.tag_operations import TagOperations
from database.database_models import Base


class DatabaseManager:
    def __init__(self):
        engine = self._get_engine()
        self._person_ops = PersonOperations(engine)
        self._group_ops = GroupOperations(engine)
        self._tag_ops = TagOperations(engine)
        self._location_ops = LocationOperations(engine)
        self._place_ops = PlaceOperations(engine)

    def _get_engine(self):
        # Format: postgresql://username:password@host:port/database_name
        username = "evidence"
        password = "evidence"
        host = "localhost"
        port = "5432"
        database = "evidence"

        database_url = f"postgresql://{username}:{password}@{host}:{port}/{database}"

        engine = create_engine(database_url, echo=False)
        Base.metadata.create_all(engine)
        return engine
    
    def groups(self) -> GroupOperations:
        return self._group_ops
    
    def people(self) -> PersonOperations:
        return self._person_ops
    
    def tags(self) -> TagOperations:
        return self._tag_ops
    
    def locations(self) -> LocationOperations:
        return self._location_ops
    
    def places(self) -> PlaceOperations:
        return self._place_ops

