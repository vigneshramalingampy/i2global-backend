from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from .database import User, Note

async def connect_to_db():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    await init_beanie(database=client.db_name, document_models=[User, Note])
