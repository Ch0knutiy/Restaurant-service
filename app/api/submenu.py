from uuid import UUID

from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import schemas
from services import submenuService
from sqlalchemy.orm import Session

router = APIRouter()


@router.get('/{menu_id}/submenus')
async def get_submenus(menu_id: UUID, db: Session = Depends(get_db)):
    return submenuService.get_submenus(menu_id, db)


@router.get('/{menu_id}/submenus/{id}')
async def get_submenu(id: UUID, db: Session = Depends(get_db)):
    submenu = submenuService.get_submenu(id, db)
    if not submenu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='submenu not found')
    return submenu


@router.post('/{menu_id}/submenus', status_code=201)
async def create_submenu(payload: schemas.SubmenuSchema, menu_id: UUID, db: Session = Depends(get_db)):
    return submenuService.create_submenu(payload, menu_id, db)


@router.patch('/{menu_id}/submenus/{id}', status_code=200)
async def update_submenu(id: UUID, payload: schemas.SubmenuSchema, db: Session = Depends(get_db)):
    submenu = submenuService.update_submenu(id, payload, db)
    if not submenu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No submenu with this id: {id} found')
    return submenu


@router.delete('/{menu_id}/submenus/{id}', status_code=200)
async def delete_submenu(id: UUID, db: Session = Depends(get_db)):
    return submenuService.delete_submenu(id, db)
