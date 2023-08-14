from uuid import UUID

from database import get_session
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from redis.asyncio import Redis
from redis_connection import get_redis
from schemas import schemas
from services import menuService
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get('/full')
async def get_menus_full(db: AsyncSession = Depends(get_session), rd: Redis = Depends(get_redis)):
    return await menuService.get_menus_full(db, rd)


@router.get('/')
async def get_menus(db: AsyncSession = Depends(get_session), rd: Redis = Depends(get_redis)):
    return await menuService.get_menus(db, rd)


@router.get('/{id}')
async def get_menu(id: UUID, db: AsyncSession = Depends(get_session), rd: Redis = Depends(get_redis)):
    menu = await menuService.get_menu(id, db, rd)
    if not menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='menu not found')
    return menu


@router.post('/', status_code=201)
async def create_menu(payload: schemas.MenuSchema, background_tasks: BackgroundTasks,
                      db: AsyncSession = Depends(get_session), rd: Redis = Depends(get_redis)):
    return await menuService.create_menu(payload, background_tasks, db, rd)


@router.patch('/{id}', status_code=200)
async def update_menu(id: UUID, payload: schemas.MenuSchema, background_tasks: BackgroundTasks,
                      db: AsyncSession = Depends(get_session), rd: Redis = Depends(get_redis)):
    menu = await menuService.update_menu(id, payload, background_tasks, db, rd)
    if not menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No menu with this id: {id} found')
    return menu


@router.delete('/{id}', status_code=200)
async def delete_menu(id: UUID, background_tasks: BackgroundTasks,
                      db: AsyncSession = Depends(get_session), rd: Redis = Depends(get_redis)):
    return await menuService.delete_menu(id, background_tasks, db, rd)
