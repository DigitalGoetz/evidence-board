from fastapi import APIRouter

router = APIRouter()


@router.get("/locations/status", tags=["locations"])
async def get_status():
    return "OK"
