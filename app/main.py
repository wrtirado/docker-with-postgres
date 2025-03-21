from fastapi import FastAPI
from app.database import engine, Base
from app.models import Item

# Initialize DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "FastAPI + Docker + Postgres is working!"}
