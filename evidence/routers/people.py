from fastapi import APIRouter, Response, status
from typing import List, Union, Dict
from evidence.pydantic_schemas.schemas import PersonBase, PersonSchema
from evidence.database.database_manager import DatabaseManager
from database.database_exceptions import ObjectNotFoundException, ObjectAlreadyExistsException, ObjectInfoExistsException, ObjectInfoDoesNotExistException
from evidence.database.database_models import PersonDb

router = APIRouter()
database = DatabaseManager()


@router.get("/people/status", tags=["people"])
async def get_status():
    return "OK"


@router.put("/people/{id}/{new_name}", tags=["people"])
async def rename_person(id: int, new_name: str, response: Response) -> Union[PersonSchema, Dict]:
    try:
        person = database.people().rename(id, new_name)
        response.status_code = status.HTTP_202_ACCEPTED
        return person
    except ObjectNotFoundException as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return e.return_dict()


@router.delete("/people/{id}", tags=["people"])
async def delete_person(id: str, response: Response) -> None:
    try:
        database.people().delete(id)
        response.status_code = status.HTTP_204_NO_CONTENT
    except ObjectNotFoundException:
        response.status_code = status.HTTP_404_NOT_FOUND
        print(f"Error in {__name__} delete_person (not found)")


@router.post("/people/", tags=["people"])
async def create_person(person: PersonBase, response: Response) -> Union[PersonSchema, Dict]:
    try:
        created_person: PersonDb = database.people().create(person.name)
        response.status_code = status.HTTP_201_CREATED
        return PersonSchema.model_validate(created_person)
    except ObjectAlreadyExistsException as e:
        response.status_code = status.HTTP_409_CONFLICT
        return e.return_dict()


@router.put("/people/tag/{person_id}/{tag_id}", tags=["people"])
async def tag_person(person_id: int, tag_id: int, response: Response) -> Union[PersonSchema, Dict]:
    try:
        person = database.people().tag(person_id, tag_id)
        response.status_code = status.HTTP_202_ACCEPTED
        return person
    except ObjectNotFoundException as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return e.return_dict()
    except ObjectInfoExistsException as e:
        response.status_code = status.HTTP_409_CONFLICT
        return e.return_dict()


@router.put("/people/untag/{person_id}/{tag_id}", tags=["people"])
async def untag_person(person_id: int, tag_name: int, response: Response) -> PersonSchema:
    try:
        person = database.people().untag(person_id, tag_name)
        response.status_code = status.HTTP_202_ACCEPTED
        return person
    except ObjectNotFoundException as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return e.return_dict()
    except ObjectInfoDoesNotExistException as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return e.return_dict()


@router.get("/people/", tags=["people"])
async def get_all() -> List[PersonSchema]:
    people_response_list: List[PersonSchema] = []
    people: List[PersonDb] = database.people().get_all()
    for person in people:
        people_response_list.append(PersonSchema.model_validate(person))
    return people_response_list


@router.get("/people/{id}", tags=["people"])
async def get_by_id(id: int, response: Response) -> Union[PersonSchema, Dict]:
    try:
        person = database.people().get_by_id(id)
        return person
    except ObjectNotFoundException as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return e.return_dict()


@router.put("/people/{person_id}/add/{group_id}", tags=["people"])
async def add_member(person_id: int, group_id: int, response: Response) -> Union[PersonSchema, Dict]:
    try:
        updated_person = database.people().add_affiliation(person_id, group_id)
        response.status_code = status.HTTP_202_ACCEPTED
        return updated_person
    except ObjectNotFoundException as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return e.return_dict()
    except ObjectInfoExistsException as e:
        response.status_code = status.HTTP_409_CONFLICT
        return e.return_dict()


@router.put("/people/{person_id}/remove/{group_id}", tags=["people"])
async def remove_member(person_id: int, group_id: int, response: Response) -> Union[PersonSchema, Dict]:
    try:
        updated_person = database.people().remove_affiliation(person_id, group_id)
        response.status_code = status.HTTP_202_ACCEPTED
        return updated_person
    except ObjectNotFoundException as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return e.return_dict()
    except ObjectInfoDoesNotExistException as e:
        response.status_code = status.HTTP_409_CONFLICT
        return e.return_dict()
