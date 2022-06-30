from typing import Optional

from fastapi import APIRouter, HTTPException
from ormar import NoMatch

from ..impl.database import User

router = APIRouter(prefix="/users")


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int) -> Optional[User]:
    """Get a user from the database."""

    try:
        user = await User.objects.get(id=user_id)
    except NoMatch:
        raise HTTPException(404, "User not found.")

    return user


@router.post("/", response_model=User, status_code=201)
async def create_or_update_user(user: User | list[User]) -> Optional[User] | list[User]:
    """Create or update a user in the database"""

    if isinstance(user, list):
        if len(user) > 10000:
            raise HTTPException(400, "You cannot send more than 10000 users during a single request.")

    if isinstance(user, User) or len(user) == 1:
        if isinstance(user, list):
            user = user[0]

        await user.save()

        return user

    await User.bulk_upsert(user)

    return user


@router.delete("/{user_id}", response_model=User)
async def delete_user(user_id: int) -> Optional[User]:
    """Deletes a user from the database."""

    try:
        user = await User.objects.get(id=user_id)
    except NoMatch:
        raise HTTPException(404, "User not found.")

    await user.delete()

    return user
