from fastapi import APIRouter

router = APIRouter()

@router.get("/people/status", tags=["people"])
async def get_status():
    return "OK"