from fastapi import APIRouter

router = APIRouter()


@router.get("/tags/status", tags=["tags"])
async def get_status():
    return "OK"
