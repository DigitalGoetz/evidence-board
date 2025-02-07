from fastapi import APIRouter, Response, status
from typing import List, Union, Dict
from evidence.pydantic.schemas import PlaceBase, PlaceSchema
from evidence.database.database_manager import DatabaseManager
from database.database_exceptions import ObjectNotFoundException, ObjectAlreadyExistsException, ObjectInfoExistsException, ObjectInfoDoesNotExistException
from evidence.database.database_models import PlaceDb

router = APIRouter()
database = DatabaseManager()


@router.get("/places/status", tags=["places"])
async def get_status():
    return "OK"


@router.put("/places/{id}/{new_name}", tags=["places"])
async def rename_place(id: int, new_name: str, response: Response) -> Union[PlaceSchema, Dict]:
    try:
        place = database.places().rename(id, new_name)
        response.status_code = status.HTTP_202_ACCEPTED
        return place
    except ObjectNotFoundException as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return e.return_dict()


@router.delete("/places/{id}", tags=["places"])
async def delete_place(id: str, response: Response) -> None:
    try:
        database.places().delete(id)
        response.status_code = status.HTTP_204_NO_CONTENT
    except ObjectNotFoundException:
        response.status_code = status.HTTP_404_NOT_FOUND
        print(f"Error in {__name__} delete_place (not found)")


@router.post("/places/", tags=["places"])
async def create_place(place: PlaceBase, response: Response) -> Union[PlaceSchema, Dict]:
    try:
        created_place: PlaceDb = database.places().create(place.name)
        response.status_code = status.HTTP_201_CREATED
        return PlaceSchema.model_validate(created_place)
    except ObjectAlreadyExistsException as e:
        response.status_code = status.HTTP_409_CONFLICT
        return e.return_dict()


@router.put("/places/tag/{place_id}/{tag_id}", tags=["places"])
async def tag_place(place_id: int, tag_id: int, response: Response) -> Union[PlaceSchema, Dict]:
    try:
        place = database.places().tag(place_id, tag_id)
        response.status_code = status.HTTP_202_ACCEPTED
        return place
    except ObjectNotFoundException as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return e.return_dict()
    except ObjectInfoExistsException as e:
        response.status_code = status.HTTP_409_CONFLICT
        return e.return_dict()


@router.put("/places/untag/{place_id}/{tag_id}", tags=["places"])
async def untag_place(place_id: int, tag_name: int, response: Response) -> PlaceSchema:
    try:
        place = database.places().untag(place_id, tag_name)
        response.status_code = status.HTTP_202_ACCEPTED
        return place
    except ObjectNotFoundException as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return e.return_dict()
    except ObjectInfoDoesNotExistException as e:
        response.status_code = status.HTTP_409_CONFLICT
        return e.return_dict()


@router.get("/places/", tags=["places"])
async def get_all() -> List[PlaceSchema]:
    places_response_list: List[PlaceSchema] = []
    places: List[PlaceDb] = database.places().get_all()
    for place in places:
        places_response_list.append(PlaceSchema.model_validate(place))
    return places_response_list


@router.get("/places/{id}", tags=["places"])
async def get_by_id(id: int, response: Response) -> Union[PlaceSchema, Dict]:
    try:
        place = database.places().get_by_id(id)
        return place
    except ObjectNotFoundException as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return e.return_dict()


@router.put("/places/{place_id}/add/{location_id}", tags=["places"])
async def set_within(place_id: int, location_id: int, response: Response) -> Union[PlaceSchema, Dict]:
    try:
        updated_place = database.places().set_within(place_id, location_id)
        response.status_code = status.HTTP_202_ACCEPTED
        return updated_place
    except ObjectNotFoundException as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return e.return_dict()
    except ObjectInfoExistsException as e:
        response.status_code = status.HTTP_409_CONFLICT
        return e.return_dict()


@router.put("/places/{place_id}/remove/{location_id}", tags=["places"])
async def remove_member(place_id: int, location_id: int, response: Response) -> Union[PlaceSchema, Dict]:
    try:
        updated_place = database.places().unset_within(place_id, location_id)
        response.status_code = status.HTTP_202_ACCEPTED
        return updated_place
    except ObjectNotFoundException as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return e.return_dict()
    except ObjectInfoDoesNotExistException as e:
        response.status_code = status.HTTP_409_CONFLICT
        return e.return_dict()
