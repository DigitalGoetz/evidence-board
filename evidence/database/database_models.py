from typing import List, Optional
from sqlalchemy import String, Enum, ForeignKey, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from evidence.database.database_enumerations import GroupType, LocationType, PersonStatus
from evidence.pydantic_schemas.schemas import GroupBase


class Base(DeclarativeBase):
    pass


def get_names(list_of_models):
    return [model.name for model in list_of_models]


tagged_groups = Table(
    "tagged_groups",
    Base.metadata,
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
)

tagged_people = Table(
    "tagged_people",
    Base.metadata,
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
    Column("people_id", ForeignKey("people.id"), primary_key=True),
)

tagged_locations = Table(
    "tagged_locations",
    Base.metadata,
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
    Column("location_id", ForeignKey("locations.id"), primary_key=True),
)

tagged_places = Table(
    "tagged_places",
    Base.metadata,
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
    Column("place_id", ForeignKey("places.id"), primary_key=True),
)

geospatial_association_table = Table(
    "geospatial_association_table",
    Base.metadata,
    Column("place_id", ForeignKey("places.id"), primary_key=True),
    Column("location_id", ForeignKey("locations.id"), primary_key=True),
)

social_association_table = Table(
    "social_association_table",
    Base.metadata,
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
    Column("person_id", ForeignKey("people.id"), primary_key=True),
)


class TagDb(Base):
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), unique=True)
    groups: Mapped[List["GroupDb"]] = relationship(secondary=tagged_groups, back_populates="tags")
    people: Mapped[List["PersonDb"]] = relationship(secondary=tagged_people, back_populates="tags")
    locations: Mapped[List["LocationDb"]] = relationship(secondary=tagged_locations, back_populates="tags")
    places: Mapped[List["PlaceDb"]] = relationship(secondary=tagged_places, back_populates="tags")

    def __repr__(self):
        return f"TagDb(id={self.id}, name={self.name})"


class GroupDb(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    type: Mapped[GroupType] = mapped_column(Enum(GroupType), nullable=False)
    members: Mapped[List["PersonDb"]] = relationship(secondary=social_association_table, back_populates="affiliations")
    tags: Mapped[List["TagDb"]] = relationship(secondary=tagged_groups, back_populates="groups")

    def __init__(self, name: str, type: GroupType, members: Optional[List[GroupBase]] = [], tags: List[str] = []) -> None:
        self.name = name
        self.type = type
        self.members = []
        if members:
            for member in members:
                self.members.append(member)
        if tags:
            for tag in tags:
                self.tags.append(tag)

    def __repr__(self):
        return f"GroupDb(id={self.id}, name={self.name}, type={self.type}, members({len(self.members)})={get_names(self.members)}, tags({get_names(self.tags)}))"


class PersonDb(Base):
    __tablename__ = "people"
    id: Mapped[int] = mapped_column(primary_key=True)
    living: Mapped[PersonStatus] = mapped_column(String(10))
    name: Mapped[str] = mapped_column(String(64))
    affiliations: Mapped[List["GroupDb"]] = relationship(secondary=social_association_table, back_populates="members")
    tags: Mapped[List["TagDb"]] = relationship(secondary=tagged_people, back_populates="people")

    def __repr__(self):
        return f"PersonDb(id={self.id}, name={self.name}, affiliations({len(self.affiliations)})={get_names(self.affiliations)})"


class LocationDb(Base):  # higher level general locations (Country, State, Region, City)
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    type: Mapped[LocationType] = mapped_column(Enum(LocationType), nullable=False)
    contains: Mapped[List["PlaceDb"]] = relationship(secondary=geospatial_association_table, back_populates="within")
    tags: Mapped[List["TagDb"]] = relationship(secondary=tagged_locations, back_populates="locations")

    def __repr__(self):
        return f"Person(id={self.id}, name={self.name}, affiliations({len(self.affiliations)})={get_names(self.affiliations)})"


class PlaceDb(Base):  # specific locations (Store, Building, Cave)
    __tablename__ = "places"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(31))
    within: Mapped[List["LocationDb"]] = relationship(secondary=geospatial_association_table, back_populates="contains")
    tags: Mapped[List["TagDb"]] = relationship(secondary=tagged_places, back_populates="places")
