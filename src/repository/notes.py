from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.models import Note, Tag, User
from src.schemas import NoteModel, NoteUpdate, NoteStatusUpdate


async def get_notes(
    skip: int,
    limit: int,
    user: User,
    db: Session
) -> List[Note]:
    return db.query(Note).filter(
        Note.user_id == user.id).offset(skip).limit(limit).all()


async def get_note(
    note_id: int,
    user: User,
    db: Session
) -> Note:
    return db.query(Note).filter(
        and_(Note.id == note_id, Note.user_id == user.id)).first()


async def create_note(
    body: NoteModel,
    user: User,
    db: Session
) -> Note:
    tags = db.query(Tag).filter(
        and_(Tag.id.in_(body.tags), Tag.user_id == user.id)).all()
    note = Note(
        title=body.title, description=body.description,
        tags=tags, user=user
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


async def remove_note(
    note_id: int,
    user: User,
    db: Session
) -> Note | None:
    note = db.query(Note).filter(
        and_(Note.id == note_id, Note.user_id == user.id)).first()
    if note:
        db.delete(note)
        db.commit()
    return note


async def update_note(
    note_id: int,
    body: NoteUpdate,
    user: User,
    db: Session
) -> Note | None:
    note = db.query(Note).filter(
        and_(Note.id == note_id, Note.user_id == user.id)).first()
    if note:
        tags = db.query(Tag).filter(
            and_(Tag.id.in_(body.tags), Tag.user_id == user.id)).all()
        note.title = body.title
        note.description = body.description
        note.done = body.done
        note.tags = tags
        db.commit()
    return note


async def update_status_note(
    note_id: int,
    body: NoteStatusUpdate,
    user: User,
    db: Session
) -> Note | None:
    note = db.query(Note).filter(
        and_(Note.id == note_id, Note.user_id == user.id)).first()
    if note:
        note.done = body.done
        db.commit()
    return note
