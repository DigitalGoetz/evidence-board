from fastapi import APIRouter, Response, status
from typing import List, Union, Dict
from evidence.pydantic_schemas.schemas import TagBase, TagSchema
from evidence.database.database_manager import DatabaseManager
from database.database_exceptions import ObjectNotFoundException, ObjectAlreadyExistsException
from evidence.database.database_models import TagDb

router = APIRouter()
database = DatabaseManager()


@router.get("/tags/status", tags=["tags"])
async def get_status():
    return "OK"


@router.put("/tags/{id}/{new_name}", tags=["tags"])
async def rename_tag(id: int, new_name: str, response: Response) -> Union[TagSchema, Dict]:
    try:
        tag = database.tags().rename(id, new_name)
        response.status_code = status.HTTP_202_ACCEPTED
        return tag
    except ObjectNotFoundException as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return e.return_dict()


@router.delete("/tags/{id}", tags=["tags"])
async def delete_tag(id: str, response: Response) -> None:
    try:
        database.tags().delete(id)
        response.status_code = status.HTTP_204_NO_CONTENT
    except ObjectNotFoundException:
        response.status_code = status.HTTP_404_NOT_FOUND
        print(f"Error in {__name__} delete_tag (not found)")


@router.post("/tags/", tags=["tags"])
async def create_tag(tag: TagBase, response: Response) -> Union[TagSchema, Dict]:
    try:
        created_tag: TagDb = database.tags().create(tag.name)
        response.status_code = status.HTTP_201_CREATED
        return TagSchema.model_validate(created_tag)
    except ObjectAlreadyExistsException as e:
        response.status_code = status.HTTP_409_CONFLICT
        return e.return_dict()


@router.get("/tags/", tags=["tags"])
async def get_all() -> List[TagSchema]:
    tag_response_list: List[TagSchema] = []
    tags: List[TagDb] = database.tags().get_all()
    for tag in tags:
        tag_response_list.append(TagSchema.model_validate(tag))
    return tag_response_list


@router.get("/tags/{id}", tags=["tags"])
async def get_by_id(id: int, response: Response) -> TagSchema:
    try:
        tag = database.tags().get_by_id(id)
        return tag
    except ObjectNotFoundException as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return e.return_dict()
