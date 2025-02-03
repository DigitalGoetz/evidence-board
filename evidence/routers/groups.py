from fastapi import APIRouter

from evidence.database.database_manager import DatabaseManager

router = APIRouter()
database = DatabaseManager()

@router.get("/groups/status", tags=["groups"])
async def get_status():
    return "OK"

@router.get("/groups/", tags=["groups"])
async def get_groups():
    groups = database.groups().get_all()
    return groups