from typing import List

from fastapi import HTTPException
from sqlalchemy import select, Result, delete, update
from sqlalchemy.ext.asyncio import AsyncSession, result
from starlette import status

from .schemas import UserBase, UserCreate, UserUpdate
from .models import User


async def read_users(session: AsyncSession) -> List[User]:
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return users

async def create_user(session: AsyncSession, user: UserCreate) -> User:
    existing_user = await session.execute(select(User).where(User.email == user.email))
    if existing_user.scalar():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email already registered"
                            )
    user = User(**user.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def read_user_by_id(session: AsyncSession, user_id: int) -> User:
    stmt = select(User).where(User.id == user_id)
    result: Result = await session.execute(stmt)
    user = result.scalars().first()
    return user


async def update_user(session: AsyncSession, user_update: UserUpdate, user_id: int):
    user = await session.get(User, user_id)
    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    await session.commit()
    return user

async def delete_user_by_id(session: AsyncSession, user_id: int):
    await session.execute(delete(User).where(User.id == user_id))
    await session.commit()



