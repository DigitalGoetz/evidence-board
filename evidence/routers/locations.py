from fastapi import APIRouter
from typing import List, Union, Dict
from evidence.pydantic.schemas import LocationBase, LocationSchema
from evidence.database.database_manager import DatabaseManager
from database.database_exceptions import ObjectNotFoundException, ObjectAlreadyExistsException, ObjectInfoExistsException, ObjectInfoDoesNotExistException
from evidence.database.database_models import LocationDb

router = APIRouter()
database = DatabaseManager()


@router.get("/locations/status", tags=["locations"])
async def get_status():
    return "OK"


@router.put("/locations/{id}/{new_name}", tags=["locations"])
async def rename_location(id: int, new_name: str) -> Union[LocationSchema, Dict]:
    try:
        location = database.locations().rename(id, new_name)
        return location
    except ObjectNotFoundException as e:
        return e.return_dict()


@router.delete("/locations/{id}", tags=["locations"])
async def delete_location(id: str) -> None:
    try:
        database.locations().delete(id)
    except ObjectNotFoundException:
        print(f"Error in {__name__} delete_location (not found)")


@router.post("/locations", tags=["locations"])
async def create_location(location: LocationBase) -> Union[LocationSchema, Dict]:
    try:
        created_location: LocationDb = database.locations().create(location.name)
        return LocationSchema.model_validate(created_location)
    except ObjectAlreadyExistsException as e:
        return e.return_dict()


@router.put("/locations/tag/{location_id}/{tag_id}", tags=["locations"])
async def tag_location(location_id: int, tag_id: int) -> Union[LocationSchema, Dict]:
    try:
        location = database.locations().tag(location_id, tag_id)
        return location
    except ObjectNotFoundException as e:
        return e.return_dict()
    except ObjectInfoExistsException as e:
        return e.return_dict()


@router.put("/locations/untag/{location_id}/{tag_id}", tags=["locations"])
async def untag_location(location_id: int, tag_name: int) -> LocationSchema:
    try:
        location = database.locations().untag(location_id, tag_name)
        return location
    except ObjectNotFoundException as e:
        return e.return_dict()
    except ObjectInfoDoesNotExistException as e:
        return e.return_dict()


@router.get("/locations/", tags=["locations"])
async def get_all() -> List[LocationSchema]:
    people_response_list: List[LocationSchema] = []
    people: List[LocationDb] = database.locations().get_all()
    for location in people:
        people_response_list.append(LocationSchema.model_validate(location))
    return people_response_list


@router.get("/locations/{id}", tags=["locations"])
async def get_by_id(id: int) -> Union[LocationSchema, Dict]:
    try:
        location = database.locations().get_by_id(id)
        return location
    except ObjectNotFoundException as e:
        return e.return_dict()


@router.put("/locations/{location_id}/add/{place_id}", tags=["locations"])
async def add_member(location_id: int, place_id: int) -> Union[LocationSchema, Dict]:
    try:
        updated_location = database.locations().add_place(location_id, place_id)
        return updated_location
    except ObjectNotFoundException as e:
        return e.return_dict()
    except ObjectInfoExistsException as e:
        return e.return_dict()


@router.put("/locations/{location_id}/remove/{place_id}", tags=["locations"])
async def remove_member(location_id: int, place_id: int) -> Union[LocationSchema, Dict]:
    try:
        updated_location = database.locations().remove_place(location_id, place_id)
        return updated_location
    except ObjectNotFoundException as e:
        return e.return_dict()
    except ObjectInfoDoesNotExistException as e:
        return e.return_dict()
