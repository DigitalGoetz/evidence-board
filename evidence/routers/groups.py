from fastapi import APIRouter
from typing import List, Union, Dict
from evidence.pydantic.schemas import GroupSchema, GroupBase
from evidence.database.database_manager import DatabaseManager
from database.database_exceptions import ObjectNotFoundException, ObjectAlreadyExistsException, ObjectInfoExistsException, ObjectInfoDoesNotExistException
from evidence.database.database_models import GroupDb

router = APIRouter()
database = DatabaseManager()


@router.get("/groups/status", tags=["groups"])
async def get_status():
    return "OK"


@router.put("/groups/{id}/{new_name}", tags=["groups"])
async def rename_group(id: int, new_name: str) -> Union[GroupSchema, Dict]:
    try:
        group = database.groups().rename(id, new_name)
        return group
    except ObjectNotFoundException as e:
        return e.return_dict()


@router.delete("/groups/{id}", tags=["groups"])
async def delete_group(id: str) -> None:
    try:
        database.groups().delete(id)
    except ObjectNotFoundException:
        print(f"Error in {__name__} delete_group (not found)")


@router.post("/groups", tags=["groups"])
async def create_group(group: GroupBase) -> Union[GroupSchema, Dict]:
    try:
        created_group: GroupDb = database.groups().create(group.name, group.type)
        return GroupSchema.model_validate(created_group)
    except ObjectAlreadyExistsException as e:
        return e.return_dict()


@router.put("/groups/tag/{group_id}/{tag_id}", tags=["groups"])
async def tag_group(group_id: int, tag_id: int) -> Union[GroupSchema, Dict]:
    try:
        group = database.groups().tag(group_id, tag_id)
        return group
    except ObjectNotFoundException as e:
        return e.return_dict()
    except ObjectInfoExistsException as e:
        return e.return_dict()


@router.put("/groups/untag/{group_id}/{tag_id}", tags=["groups"])
async def untag_group(group_id: int, tag_name: int) -> GroupSchema:
    try:
        group = database.groups().untag(group_id, tag_name)
        return group
    except ObjectNotFoundException as e:
        return e.return_dict()
    except ObjectInfoDoesNotExistException as e:
        return e.return_dict()


@router.get("/groups/", tags=["groups"])
async def get_all() -> List[GroupSchema]:
    group_response_list: List[GroupSchema] = []
    groups: List[GroupDb] = database.groups().get_all()
    for group in groups:
        group_response_list.append(GroupSchema.model_validate(group))
    return group_response_list


@router.get("/groups/{id}", tags=["groups"])
async def get_by_id(id: int) -> Union[GroupSchema, Dict]:
    try:
        group = database.groups().get_by_id(id)
        return group
    except ObjectNotFoundException as e:
        return e.return_dict()


@router.put("/groups/{group_id}/add/{person_id}", tags=["groups"])
async def add_member(group_id: int, person_id: int) -> Union[GroupSchema, Dict]:
    try:
        updated_group = database.groups().add_member(group_id, person_id)
        return updated_group
    except ObjectNotFoundException as e:
        return e.return_dict()
    except ObjectInfoExistsException as e:
        return e.return_dict()


@router.put("/groups/{group_id}/remove/{person_id}", tags=["groups"])
async def remove_member(group_id: int, person_id: int) -> Union[GroupSchema, Dict]:
    try:
        updated_group = database.groups().remove_member(group_id, person_id)
        return updated_group
    except ObjectNotFoundException as e:
        return e.return_dict()
    except ObjectInfoDoesNotExistException as e:
        return e.return_dict()
