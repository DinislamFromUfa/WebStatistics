from typing import List

from sqlalchemy import select, Result, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import UserBase
from .models import User


async def read_users(session: AsyncSession) -> List[User]:
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return users

async def create_user(session: AsyncSession, user: UserBase) -> User:
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

async def delete_user_by_id(session: AsyncSession, user_id: int):
    stmt = select(User).where(User.id == user_id)
    result: Result = await session.execute(stmt)
    user = result.scalars().first()
    if user:
        stmt = delete(User).where(User.id == user_id)
        await session.execute(stmt)
        await session.commit()
        return user
    else:
        return None



