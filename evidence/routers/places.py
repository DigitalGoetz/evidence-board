from fastapi import APIRouter

router = APIRouter()


@router.get("/places/status", tags=["places"])
async def get_status():
    return "OK"
