from uuid import UUID

from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import schemas
from services import menuService
from sqlalchemy.orm import Session

router = APIRouter()


@router.get('/')
async def get_menus(db: Session = Depends(get_db)):
    return menuService.get_menus(db)


@router.get('/{id}')
async def get_menu(id: UUID, db: Session = Depends(get_db)):
    menu = menuService.get_menu(id, db)
    if not menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='menu not found')
    return menu


@router.post('/', status_code=201)
async def create_menu(payload: schemas.MenuSchema, db: Session = Depends(get_db)):
    return menuService.create_menu(payload, db)


@router.patch('/{id}', status_code=200)
async def update_menu(id: UUID, payload: schemas.MenuSchema, db: Session = Depends(get_db)):
    menu = menuService.update_menu(id, payload, db)
    if not menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No menu with this id: {id} found')
    return menu


@router.delete('/{id}', status_code=200)
async def delete_menu(id: UUID, db: Session = Depends(get_db)):
    return menuService.delete_menu(id, db)
