from uuid import UUID

from database import get_session
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from redis.asyncio import Redis
from redis_connection import get_redis
from schemas import schemas
from services import submenuService
from sqlalchemy.orm import Session

router = APIRouter()


@router.get('/{menu_id}/submenus')
async def get_submenus(menu_id: UUID, db: Session = Depends(get_session), rd: Redis = Depends(get_redis)):
    return await submenuService.get_submenus(menu_id, db, rd)


@router.get('/{menu_id}/submenus/{id}')
async def get_submenu(id: UUID, db: Session = Depends(get_session), rd: Redis = Depends(get_redis)):
    submenu = await submenuService.get_submenu(id, db, rd)
    if not submenu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='submenu not found')
    return submenu


@router.post('/{menu_id}/submenus', status_code=201)
async def create_submenu(payload: schemas.SubmenuSchema, menu_id: UUID, background_tasks: BackgroundTasks,
                         db: Session = Depends(get_session), rd: Redis = Depends(get_redis)):
    return await submenuService.create_submenu(payload, menu_id, background_tasks, db, rd)


@router.patch('/{menu_id}/submenus/{id}', status_code=200)
async def update_submenu(id: UUID, menu_id: UUID, payload: schemas.SubmenuSchema, background_tasks: BackgroundTasks,
                         db: Session = Depends(get_session), rd: Redis = Depends(get_redis)):
    submenu = await submenuService.update_submenu(id, menu_id, payload, background_tasks, db, rd)
    if not submenu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No submenu with this id: {id} found')
    return submenu


@router.delete('/{menu_id}/submenus/{id}', status_code=200)
async def delete_submenu(id: UUID, menu_id: UUID, background_tasks: BackgroundTasks,
                         db: Session = Depends(get_session), rd: Redis = Depends(get_redis)):
    return await submenuService.delete_submenu(id, menu_id, background_tasks, db, rd)
