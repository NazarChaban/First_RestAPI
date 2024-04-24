from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.schemas import NoteModel, NoteResponse, NoteUpdate, NoteStatusUpdate
from src.repository import notes as repository_notes
from src.services.auth import auth_service
from src.database.models import User
from src.database.db import get_db

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/", response_model=List[NoteResponse],
    description='No more than 10 requests per minute',
    dependencies=[Depends(RateLimiter(times=10, minutes=1))]
)
async def read_notes(
    skip: int = 0,
    limit: int = 100,
    curr_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    return await repository_notes.get_notes(skip, limit, curr_user, db)


@router.get("/{note_id}", response_model=NoteResponse)
async def read_note(
    note_id: int,
    curr_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    note = await repository_notes.get_note(note_id, curr_user, db)
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return note


@router.post(
    "/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED
)
async def create_note(
    body: NoteModel,
    curr_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    return await repository_notes.create_note(body, curr_user, db)


@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    body: NoteUpdate,
    note_id: int,
    curr_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    note = await repository_notes.update_note(note_id, body, curr_user, db)
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return note


@router.patch("/{note_id}", response_model=NoteResponse)
async def update_status_note(
    body: NoteStatusUpdate,
    note_id: int,
    curr_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    note = await repository_notes.update_status_note(
        note_id, body, curr_user, db
    )
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return note


@router.delete("/{note_id}", response_model=NoteResponse)
async def remove_note(
    note_id: int,
    curr_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    note = await repository_notes.remove_note(note_id, curr_user, db)
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return note
