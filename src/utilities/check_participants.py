from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from crud.user import user_crud
from models import User


async def check_chat_participants(
    db: AsyncSession, participants: List[int], chat_owner_id: int
) -> List[User]:
    checked_participants = []
    if len(participants) >= 1:
        for participant in participants:
            found_user = await user_crud.get_by_id(db=db, obj_id=participant)
            if found_user is None:
                raise Exception("User not found")
            if found_user.id == chat_owner_id:
                raise Exception(
                    "You cannot add yourself to the chat participants!"
                )
            if found_user in checked_participants:
                raise Exception("You cannot add one user to the chat twice!")
            checked_participants.append(found_user)
        return checked_participants
    return checked_participants
