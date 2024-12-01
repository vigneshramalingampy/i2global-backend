from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.i2global_backend.api.database.database_setup import connect_to_db


@asynccontextmanager
async def lifespan(app : FastAPI) -> None:
    await connect_to_db()
    yield