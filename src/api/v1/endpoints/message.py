from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from api.dependencies.auth import get_current_user
from api.dependencies.database import get_async_db
from constants.remove_type import RemoveMessageType
from crud.chat import chat_crud
from crud.delete_for_user import delete_for_user_crud
from crud.message import message_crud
from models import User
from schemas.message import MessageCreate, MessageResponse
from services import message as message_service

router = APIRouter()


@router.get("/sent/{chat_id}/", response_model=List[MessageResponse])
async def read_all_sent_by_chat_id(
    chat_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_async_db),
):
    """
    Просмотр всех сообщений отправленных пользователем
    в определенный  чат
    """
    if found_chat := await chat_crud.get_by_id_and_user_id(
        db=db, user_id=current_user.id, obj_id=chat_id
    ):
        found_messages = await message_crud.get_by_chat_id_and_author_id(
            db=db, author_id=current_user.id, chat_id=found_chat.id
        )
        return found_messages
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
    )


@router.get("/{chat_id}/", response_model=List[MessageResponse])
async def read_chat_messages(
    chat_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_async_db),
):
    """
    Просмотр истории чата
    """
    if found_chat := await chat_crud.get_by_id_and_user_id(
        db=db, user_id=current_user.id, obj_id=chat_id
    ):
        found_messages = await message_crud.get_by_chat_id_and_user_id(
            db=db, user_id=current_user.id, chat_id=found_chat.id
        )
        return found_messages
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
    )


@router.get("/message/{message_id}/", response_model=MessageResponse)
async def read_message(
    message_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_async_db),
):
    """
    Чтение одного опрделенного сообщения по ID
    """
    if found_message := await message_crud.get_by_id_and_user_id(
        db=db, user_id=current_user.id, obj_id=message_id
    ):
        return found_message
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
    )


@router.post("/{chat_id}/", status_code=status.HTTP_201_CREATED)
async def create_message(
    chat_id: int,
    message: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_async_db),
):
    found_chat = await chat_crud.get_by_id_and_user_id(
        db=db, obj_id=chat_id, user_id=current_user.id
    )
    if not found_chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
        )
    try:
        await message_service.create(
            db=db,
            create_data=message,
            chat_id=found_chat.id,
            author_id=current_user.id,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.delete("/{message_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def remove_message(
    message_id: int,
    remove_type: RemoveMessageType = Query(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_async_db),
) -> None:
    if found_message := await message_crud.get_by_id_and_user_id(
        db=db, user_id=current_user.id, obj_id=message_id
    ):
        if remove_type == RemoveMessageType.FOR_ALL:
            if found_message.author_id == current_user.id:
                return await message_crud.mark_deleted(
                    db=db, user_id=current_user.id, message_id=found_message.id
                )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You have not permission",
            )
        if remove_type == RemoveMessageType.FOR_ME:
            return await delete_for_user_crud.create_by_message_id_and_user_id(
                db=db, user_id=current_user.id, message_id=found_message.id
            )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
    )
