from sqlalchemy import create_engine

from database.operations.group_operations import GroupDbOperations
from database.operations.person_operations import PersonDbOperations
from database.operations.place_operations import PlaceDbOperations
from database.operations.location_operations import LocationDbOperations
from database.operations.tag_operations import TagDbOperations
from database.database_models import Base


class DatabaseManager:
    def __init__(self):
        engine = self._get_engine()
        self._person_ops = PersonDbOperations(engine)
        self._group_ops = GroupDbOperations(engine)
        self._tag_ops = TagDbOperations(engine)
        self._location_ops = LocationDbOperations(engine)
        self._place_ops = PlaceDbOperations(engine)

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

    def groups(self) -> GroupDbOperations:
        return self._group_ops

    def people(self) -> PersonDbOperations:
        return self._person_ops

    def tags(self) -> TagDbOperations:
        return self._tag_ops

    def locations(self) -> LocationDbOperations:
        return self._location_ops

    def places(self) -> PlaceDbOperations:
        return self._place_ops
