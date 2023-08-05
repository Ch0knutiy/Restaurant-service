from uuid import UUID

from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import schemas
from services import dishService
from sqlalchemy.orm import Session

router = APIRouter()


@router.get('/{menu_id}/submenus/{submenu_id}/dishes')
async def get_dishes(submenu_id: UUID, db: Session = Depends(get_db)):
    return dishService.get_dishes(submenu_id, db)


@router.get('/{menu_id}/submenus/{submenu_id}/dishes/{id}')
async def get_dish(id: UUID, db: Session = Depends(get_db)):
    dish = dishService.get_dish(id, db)
    if not dish:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='dish not found')
    return dish


@router.post('/{menu_id}/submenus/{submenu_id}/dishes', status_code=201)
def create_dish(payload: schemas.DishSchema, submenu_id: UUID, db: Session = Depends(get_db)):
    return dishService.create_dish(payload, submenu_id, db)


@router.patch('/{menu_id}/submenus/{submenu_id}/dishes/{id}', status_code=200)
async def update_dish(id: UUID, payload: schemas.DishSchema, db: Session = Depends(get_db)):
    dish = dishService.update_dish(id, payload, db)
    if not dish:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No submenu with this id: {id} found')
    return dish


@router.delete('/{menu_id}/submenus/{submenu_id}/dishes/{id}', status_code=200)
async def delete_dish(id: UUID, db: Session = Depends(get_db)):
    return dishService.delete_dish(id, db)
