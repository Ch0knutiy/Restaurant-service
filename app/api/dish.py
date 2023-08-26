from uuid import UUID

from database import get_session
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from redis.asyncio import Redis
from redis_connection import get_redis
from schemas import schemas
from services import dishService
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get('/{menu_id}/submenus/{submenu_id}/dishes', response_model=list[schemas.ResponseDish])
async def get_dishes(submenu_id: UUID, db: AsyncSession = Depends(get_session), rd: Redis = Depends(get_redis)):
    return await dishService.get_dishes(submenu_id, db, rd)


@router.get('/{menu_id}/submenus/{submenu_id}/dishes/{id}', response_model=schemas.ResponseDish,
            responses={404: {'model': schemas.Message}})
async def get_dish(id: UUID, db: AsyncSession = Depends(get_session), rd: Redis = Depends(get_redis)):
    dish = await dishService.get_dish(id, db, rd)
    if not dish:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='dish not found')
    return dish


@router.post('/{menu_id}/submenus/{submenu_id}/dishes', response_model=schemas.ResponseDish, status_code=201)
async def create_dish(payload: schemas.DishSchema, submenu_id: UUID, menu_id: UUID, background_tasks: BackgroundTasks,
                      db: AsyncSession = Depends(get_session), rd: Redis = Depends(get_redis)):
    return await dishService.create_dish(payload, submenu_id, menu_id, background_tasks, db, rd)


@router.patch('/{menu_id}/submenus/{submenu_id}/dishes/{id}', response_model=schemas.ResponseDish, status_code=200,
              responses={404: {'model': schemas.Message}})
async def update_dish(id: UUID, submenu_id: UUID, payload: schemas.DishSchema, background_tasks: BackgroundTasks,
                      db: AsyncSession = Depends(get_session), rd: Redis = Depends(get_redis)):
    dish = await dishService.update_dish(id, submenu_id, payload, background_tasks, db, rd)
    if not dish:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No submenu with this id: {id} found')
    return dish


@router.delete('/{menu_id}/submenus/{submenu_id}/dishes/{id}', response_model=schemas.Delete, status_code=200)
async def delete_dish(id: UUID, submenu_id: UUID, menu_id: UUID, background_tasks: BackgroundTasks,
                      db: AsyncSession = Depends(get_session), rd: Redis = Depends(get_redis)):
    return await dishService.delete_dish(id, submenu_id, menu_id, background_tasks, db, rd)
