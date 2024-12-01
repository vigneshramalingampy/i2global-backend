from pydantic import Field
from datetime import datetime, timezone

from typing import List, Optional
from pydantic import EmailStr
import uuid

from beanie import Document, Link


class Note(Document):
    note_id: uuid.UUID = uuid.uuid4()
    note_title: str
    note_content: str
    last_update: datetime = datetime.now(timezone.utc)
    created_on: datetime = datetime.now(timezone.utc)

    class Settings:
        name = "notes"


class User(Document):
    user_id: uuid.UUID = uuid.uuid4()
    user_name: str
    user_email: EmailStr
    mobile_number: str
    password: str
    refresh_tokens: Optional[List[str]] = Field(default_factory=list)
    last_update: datetime = datetime.now(timezone.utc)
    created_on: datetime = datetime.now(timezone.utc)
    notes: Optional[List[Link[Note]]] = Field(default_factory=list)

    class Settings:
        name = "users"
