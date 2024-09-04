from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from crud.user import user_crud
from models import User


async def check_chat_participants(
    db: AsyncSession, participants: List[int], chat_owner: User
) -> List[User]:
    if len(participants) >= 1:
        checked_participants = []
        for participant in participants:
            found_user = await user_crud.get_by_id(db=db, obj_id=participant)
            if not found_user:
                raise Exception("User not found")
            else:
                if participants.count(found_user.id) > 1:
                    raise Exception(
                        "You cannot add one user to the chat twice!"
                    )
                if found_user.id == chat_owner.id:
                    raise Exception(
                        "You cannot add yourself to the chat participants!"
                    )
                checked_participants.append(found_user)
        return checked_participants
    return participants
