from datetime import datetime, timezone
from typing import List
from uuid import UUID

from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, HTTPException
from src.i2global_backend.api.database.database import Note
from src.i2global_backend.api.notes.schema import (
    NoteCreate,
    NoteUpdate,
    NoteResponse,
    BaseResponse,
    ErrorResponse,
)

notes_router = APIRouter(prefix="/notes",tags=["notes router (protected)"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

@notes_router.get("/get", response_model=List[NoteResponse])
async def get_all_notes():
    notes = await Note.find_all().to_list()
    return notes

# Get note by ID
@notes_router.get("/get/{note_id}", response_model=NoteResponse)
async def get_note(note_id: UUID):
    note = await Note.find_one(Note.note_id == note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@notes_router.post("/create", response_model=NoteResponse)
async def create_note(note_data: NoteCreate) -> NoteResponse:
    new_note = Note(**note_data.model_dump())
    await new_note.insert()
    return new_note


@notes_router.put("/update/{note_id}", response_model=NoteResponse)
async def update_note(note_id: UUID, note_data: NoteUpdate) -> NoteResponse:
    note = await Note.find_one(Note.note_id == note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    update_data = note_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(note, key, value)
    note.last_update = datetime.now(timezone.utc)

    await note.save()
    return note

@notes_router.delete("/notes/{note_id}")
async def delete_note(note_id: UUID) -> BaseResponse:
    note = await Note.find_one(Note.note_id == note_id).delete()
    if not note:
        raise ErrorResponse(status = "error", message = "Not found")
    return BaseResponse(status= "success", message = "Note deleted successfully")
