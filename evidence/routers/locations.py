from fastapi import APIRouter, Response, status
from typing import List, Union, Dict
from evidence.pydantic.schemas import LocationBase, LocationSchema
from evidence.database.database_manager import DatabaseManager
from database.database_exceptions import ObjectNotFoundException, ObjectAlreadyExistsException, ObjectInfoExistsException, ObjectInfoDoesNotExistException
from database.database_enumerations import LocationType
from evidence.database.database_models import LocationDb

router = APIRouter()
database = DatabaseManager()


@router.get("/locations/status", tags=["locations"])
async def get_status():
    return "OK"

@router.get("/locations/types", tags=["locations"])
async def get_types():
    return [type.value for type in LocationType]


@router.put("/locations/{id}/{new_name}", tags=["locations"])
async def rename_location(id: int, new_name: str, response: Response) -> Union[LocationSchema, Dict]:
    try:
        location = database.locations().rename(id, new_name)
        response.status_code = status.HTTP_202_ACCEPTED
        return location
    except ObjectNotFoundException as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return e.return_dict()


@router.delete("/locations/{id}", tags=["locations"])
async def delete_location(id: str, response: Response) -> None:
    try:
        database.locations().delete(id)
        response.status_code = status.HTTP_204_NO_CONTENT
    except ObjectNotFoundException:
        response.status_code = status.HTTP_404_NOT_FOUND
        print(f"Error in {__name__} delete_location (not found)")


@router.post("/locations/", tags=["locations"])
async def create_location(location: LocationBase, response: Response) -> Union[LocationSchema, Dict]:
    try:
        created_location: LocationDb = database.locations().create(location.name, location.type)
        response.status_code = status.HTTP_201_CREATED
        return LocationSchema.model_validate(created_location)
    except ObjectAlreadyExistsException as e:
        response.status_code = status.HTTP_409_CONFLICT
        return e.return_dict()


@router.put("/locations/tag/{location_id}/{tag_id}", tags=["locations"])
async def tag_location(location_id: int, tag_id: int, response: Response) -> Union[LocationSchema, Dict]:
    try:
        location = database.locations().tag(location_id, tag_id)
        response.status_code = status.HTTP_202_ACCEPTED
        return location
    except ObjectNotFoundException as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return e.return_dict()
    except ObjectInfoExistsException as e:
        response.status_code = status.HTTP_409_CONFLICT
        return e.return_dict()


@router.put("/locations/untag/{location_id}/{tag_id}", tags=["locations"])
async def untag_location(location_id: int, tag_name: int, response: Response) -> LocationSchema:
    try:
        location = database.locations().untag(location_id, tag_name)
        response.status_code = status.HTTP_202_ACCEPTED
        return location
    except ObjectNotFoundException as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return e.return_dict()
    except ObjectInfoDoesNotExistException as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return e.return_dict()


@router.get("/locations/", tags=["locations"])
async def get_all() -> List[LocationSchema]:
    people_response_list: List[LocationSchema] = []
    people: List[LocationDb] = database.locations().get_all()
    for location in people:
        people_response_list.append(LocationSchema.model_validate(location))
    return people_response_list


@router.get("/locations/{id}", tags=["locations"])
async def get_by_id(id: int, response: Response) -> Union[LocationSchema, Dict]:
    try:
        location = database.locations().get_by_id(id)
        return location
    except ObjectNotFoundException as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return e.return_dict()


@router.put("/locations/{location_id}/add/{place_id}", tags=["locations"])
async def add_member(location_id: int, place_id: int, response: Response) -> Union[LocationSchema, Dict]:
    try:
        updated_location = database.locations().add_place(location_id, place_id)
        response.status_code = status.HTTP_202_ACCEPTED
        return updated_location
    except ObjectNotFoundException as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return e.return_dict()
    except ObjectInfoExistsException as e:
        response.status_code = status.HTTP_409_CONFLICT
        return e.return_dict()


@router.put("/locations/{location_id}/remove/{place_id}", tags=["locations"])
async def remove_member(location_id: int, place_id: int, response: Response) -> Union[LocationSchema, Dict]:
    try:
        updated_location = database.locations().remove_place(location_id, place_id)
        response.status_code = status.HTTP_202_ACCEPTED
        return updated_location
    except ObjectNotFoundException as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return e.return_dict()
    except ObjectInfoDoesNotExistException as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return e.return_dict()
