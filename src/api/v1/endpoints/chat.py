from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.dependencies.auth import get_current_user
from api.dependencies.database import get_async_db
from crud.chat import chat_crud
from models import User
from schemas.chat import ChatCreate, ChatResponse
from services import chat as chat_service

router = APIRouter()


@router.get("/by_chat_owner/", response_model=List[ChatResponse])
async def read_chats_by_owner(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_async_db),
):
    """
    Просмотр чатов с участниками которые создал пользователь
    """
    found_chats = await chat_crud.get_by_owner_id(
        db=db, owner_id=current_user.id
    )
    return found_chats


@router.get("/by_chat_participant/", response_model=List[ChatResponse])
async def read_chats_by_participant(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_async_db),
):
    """
    Просмотр чатов с участникаи, где пользователь - участник
    """
    found_chats = await chat_crud.get_by_participant_id(
        db=db, participant_id=current_user.id
    )
    return found_chats


@router.get("/{chat_id}/", response_model=ChatResponse)
async def read_chat(
    chat_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_async_db),
):
    """
    Просмотр чата по ID чата
    """
    if found_chat := await chat_crud.get_by_id_and_user_id(
        db=db, obj_id=chat_id, user_id=current_user.id
    ):
        return found_chat
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_chat(
    chat: ChatCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_async_db),
):
    try:
        return await chat_service.create(
            db=db, create_data=chat, user_id=current_user.id
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
