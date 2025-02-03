from pydantic import BaseModel
from typing import List


class TagModel(BaseModel):
    name: str

class PersonModel(BaseModel):
    name: str
    tags: List[TagModel]

class GroupModel(BaseModel):
    name: str
    type: str
    tags: List[TagModel]
