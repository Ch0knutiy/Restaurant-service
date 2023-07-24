from schemas import schemas
from models import models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from database import get_db


router = APIRouter()


@router.get("/{menu_id}/submenus")
async def get_submenus(menu_id, db: Session = Depends(get_db)):
    return db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id).all()


@router.get("/{menu_id}/submenus/{id}")
async def get_submenu(id, db: Session = Depends(get_db)):
    submenu = db.query(models.Submenu).filter(models.Submenu.id == id).first()
    if not submenu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"submenu not found")
    return submenu


@router.post("/{menu_id}/submenus", status_code=201)
def create_submenu(payload: schemas.SubmenuSchema, menu_id, db: Session = Depends(get_db)):
    submenu = models.Submenu(**payload.model_dump(), menu_id=menu_id)
    menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    menu.submenus_count += 1
    db.add(submenu)
    db.commit()
    db.refresh(submenu)
    return submenu


@router.patch("/{menu_id}/submenus/{id}", status_code=200)
async def update_submenu(id, payload: schemas.SubmenuSchema, db: Session = Depends(get_db)):
    submenu_query = db.query(models.Submenu).filter(models.Submenu.id == id)
    db_submenu = submenu_query.first()

    if not db_submenu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No submenu with this id: {id} found')
    update_data = payload.model_dump(exclude_unset=True)
    submenu_query.filter(models.Submenu.id == id).update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(db_submenu)
    return db_submenu


@router.delete("/{menu_id}/submenus/{id}", status_code=200)
async def delete_submenu(id, menu_id, db: Session = Depends(get_db)):
    submenu_query = db.query(models.Submenu).filter(models.Submenu.id == id)
    submenu = submenu_query.first()
    if not submenu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No submenu with this id: {id} found')
    menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    menu.submenus_count -= 1
    menu.dishes_count -= submenu.dishes_count
    submenu_query.delete(synchronize_session=False)
    db.commit()
    return {"ok": True}
