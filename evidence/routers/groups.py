from fastapi import APIRouter
from typing import List
from evidence.pydantic.schemas import GroupSchema, GroupBase
from evidence.database.database_manager import DatabaseManager
from evidence.database.database_models import GroupDb

router = APIRouter()
database = DatabaseManager()

@router.get("/groups/status", tags=["groups"])
async def get_status():
    return "OK"

@router.get("/groups/", tags=["groups"])
async def get_groups() -> List[GroupSchema]:
    group_response_list: List[GroupSchema] = []
    groups: List[GroupDb] = database.groups().get_all()
    for group in groups:
        # TODO update to latest approach
        group_response_list.append(GroupSchema.model_validate(group))
    return group_response_list

@router.post("/groups", tags=["groups"])
async def create_group(group: GroupBase) -> GroupSchema:
    created_group: GroupDb = database.groups().create(group.name, group.type)
    print(created_group)
    return GroupSchema.model_validate(created_group)
