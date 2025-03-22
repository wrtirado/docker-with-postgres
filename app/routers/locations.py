from fastapi import APIRouter


router = APIRouter()


@router.get("/")
def read_storage_locations():
    return {"message": "FastAPI + Docker + Postgres is working!"}
