from fastapi import APIRouter
from typing import List, Union, Dict
from evidence.pydantic.schemas import PersonBase, PersonSchema
from evidence.database.database_manager import DatabaseManager
from database.database_exceptions import ObjectNotFoundException, ObjectAlreadyExistsException, ObjectInfoExistsException, ObjectInfoDoesNotExistException
from evidence.database.database_models import PersonDb

router = APIRouter()
database = DatabaseManager()


@router.get("/people/status", tags=["people"])
async def get_status():
    return "OK"


@router.put("/people/{id}/{new_name}", tags=["people"])
async def rename_person(id: int, new_name: str) -> Union[PersonSchema, Dict]:
    try:
        person = database.people().rename(id, new_name)
        return person
    except ObjectNotFoundException as e:
        return e.return_dict()


@router.delete("/people/{id}", tags=["people"])
async def delete_person(id: str) -> None:
    try:
        database.people().delete(id)
    except ObjectNotFoundException:
        print(f"Error in {__name__} delete_person (not found)")


@router.post("/people", tags=["people"])
async def create_person(person: PersonBase) -> Union[PersonSchema, Dict]:
    try:
        created_person: PersonDb = database.people().create(person.name)
        return PersonSchema.model_validate(created_person)
    except ObjectAlreadyExistsException as e:
        return e.return_dict()


@router.put("/people/tag/{person_id}/{tag_id}", tags=["people"])
async def tag_person(person_id: int, tag_id: int) -> Union[PersonSchema, Dict]:
    try:
        person = database.people().tag(person_id, tag_id)
        return person
    except ObjectNotFoundException as e:
        return e.return_dict()
    except ObjectInfoExistsException as e:
        return e.return_dict()


@router.put("/people/untag/{person_id}/{tag_id}", tags=["people"])
async def untag_person(person_id: int, tag_name: int) -> PersonSchema:
    try:
        person = database.people().untag(person_id, tag_name)
        return person
    except ObjectNotFoundException as e:
        return e.return_dict()
    except ObjectInfoDoesNotExistException as e:
        return e.return_dict()


@router.get("/people/", tags=["people"])
async def get_all() -> List[PersonSchema]:
    people_response_list: List[PersonSchema] = []
    people: List[PersonDb] = database.people().get_all()
    for person in people:
        people_response_list.append(PersonSchema.model_validate(person))
    return people_response_list


@router.get("/people/{id}", tags=["people"])
async def get_by_id(id: int) -> Union[PersonSchema, Dict]:
    try:
        person = database.people().get_by_id(id)
        return person
    except ObjectNotFoundException as e:
        return e.return_dict()


@router.put("/people/{person_id}/add/{group_id}", tags=["people"])
async def add_member(person_id: int, group_id: int) -> Union[PersonSchema, Dict]:
    try:
        updated_person = database.people().add_affiliation(person_id, group_id)
        return updated_person
    except ObjectNotFoundException as e:
        return e.return_dict()
    except ObjectInfoExistsException as e:
        return e.return_dict()


@router.put("/people/{person_id}/remove/{group_id}", tags=["people"])
async def remove_member(person_id: int, group_id: int) -> Union[PersonSchema, Dict]:
    try:
        updated_person = database.people().remove_affiliation(person_id, group_id)
        return updated_person
    except ObjectNotFoundException as e:
        return e.return_dict()
    except ObjectInfoDoesNotExistException as e:
        return e.return_dict()
