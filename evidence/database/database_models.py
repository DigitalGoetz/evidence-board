from enum import StrEnum
from typing import List
from sqlalchemy import String, Enum, ForeignKey, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class ObjectType(StrEnum):
    GROUP = "group"
    PERSON = "person"
    LOCATION = "location"
    PLACE = "place"


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


class Tag(Base):
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), unique=True)
    groups: Mapped[List["Group"]] = relationship(secondary=tagged_groups, back_populates="tags")
    people: Mapped[List["Person"]] = relationship(secondary=tagged_people, back_populates="tags")
    locations: Mapped[List["Location"]] = relationship(secondary=tagged_locations, back_populates="tags")
    places: Mapped[List["NamedPlace"]] = relationship(secondary=tagged_places, back_populates="tags")

    def __repr__(self):
        return f"Tag(id={self.id}, name={self.name})"


# Social ORMs
class GroupType(StrEnum):
    COMPANY = "company"
    ORGANIZATION = "organization"
    FAMILY = "family"


social_association_table = Table(
    "social_association_table",
    Base.metadata,
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
    Column("person_id", ForeignKey("people.id"), primary_key=True),
)


class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    type: Mapped[GroupType] = mapped_column(Enum(GroupType), nullable=False)
    members: Mapped[List["Person"]] = relationship(secondary=social_association_table, back_populates="affiliations")
    tags: Mapped[List["Tag"]] = relationship(secondary=tagged_groups, back_populates="groups")

    def __repr__(self):
        return f"Group(id={self.id}, name={self.name}, type={self.type}, members({len(self.members)})={get_names(self.members)})"


class Person(Base):
    __tablename__ = "people"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    affiliations: Mapped[List["Group"]] = relationship(secondary=social_association_table, back_populates="members")
    tags: Mapped[List["Tag"]] = relationship(secondary=tagged_people, back_populates="people")

    def __repr__(self):
        return f"Person(id={self.id}, name={self.name}, affiliations({len(self.affiliations)})={get_names(self.affiliations)})"


# Geospatial ORMs


class LocationType(StrEnum):
    COUNTRY = "country"
    REGION = "region"
    STATE = "state"
    CITY = "city"

    def get_place_types(self) -> List[str]:
        place_types = [
            LocationType.COUNTRY,
            LocationType.REGION,
            LocationType.STATE,
            LocationType.CITY,
        ]
        return place_types


geospatial_association_table = Table(
    "geospatial_association_table",
    Base.metadata,
    Column("place_id", ForeignKey("places.id"), primary_key=True),
    Column("location_id", ForeignKey("locations.id"), primary_key=True),
)


class Location(Base):  # higher level general locations (Country, State, Region, City)
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    type: Mapped[LocationType] = mapped_column(Enum(LocationType), nullable=False)
    contains: Mapped[List["NamedPlace"]] = relationship(secondary=geospatial_association_table, back_populates="within")
    tags: Mapped[List["Tag"]] = relationship(secondary=tagged_locations, back_populates="locations")


class NamedPlace(Base):  # specific locations (Store, Building, Cave)
    __tablename__ = "places"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(31))
    within: Mapped[List["Location"]] = relationship(secondary=geospatial_association_table, back_populates="contains")
    tags: Mapped[List["Tag"]] = relationship(secondary=tagged_places, back_populates="places")
