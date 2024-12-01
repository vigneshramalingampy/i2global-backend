from pydantic import BaseModel

class ErrorResponse(BaseModel):
    status: str
    message: str

class BaseResponse(BaseModel):
    status: str
    message: str

class NoteCreate(BaseModel):
    note_title: str
    note_content: str

class NoteUpdate(BaseModel):
    note_title: str | None = None
    note_content: str | None = None

class NoteResponse(BaseModel):
    note_title: str
    note_content: str
