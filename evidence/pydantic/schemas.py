from pydantic import BaseModel
from typing import List


class TagBase(BaseModel):
    name: str
    class Config:
        from_attributes = True

class TagSchema(TagBase):
    id: int
    groups: List["GroupBase"]
    people: List["PersonBase"]
    locations: List["LocationBase"]
    places: List["PlaceBase"]

class PersonBase(BaseModel):
    name: str
    class Config:
        from_attributes = True

class PersonSchema(PersonBase):
    id: int
    affiliations: List["GroupBase"]
    tags: List[TagBase]

class GroupBase(BaseModel):
    name: str
    type: str
    class Config:
        from_attributes = True

class GroupSchema(GroupBase):
    id: int
    tags: List[TagBase]
    members: List["PersonBase"]

class LocationBase(BaseModel):
    name: str
    type: str
    class Config:
        from_attributes = True

class LocationSchema(LocationBase):
    id: int
    contains: List["PlaceBase"]
    tags: List[TagBase]

class PlaceBase(BaseModel):
    name: str
    class Config:
        from_attributes = True

class PlaceSchema(PlaceBase):
    id: int
    tags: List[TagBase]
    within: List["LocationBase"]
