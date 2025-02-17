from typing import List
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import UserCreate
from .database import get_db
from .schemas import UserBase
from .usercrud import read_users, create_user, read_user_by_id, delete_user_by_id

router = APIRouter(tags=["users"])

@router.get("/", response_model=List[UserBase])
async def get_users(session: AsyncSession = Depends(get_db)):
    return await read_users(session=session)

@router.post("/", response_model=UserCreate, status_code=201)
async def make_user(user: UserCreate, session: AsyncSession = Depends(get_db)):
    return await create_user(session=session, user=user)

@router.get('/{user_id}/', response_model=UserBase)
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_db)):
    user = await read_user_by_id(session=session, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}/", response_model=UserBase)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_db)):
    user = await delete_user_by_id(session=session, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

