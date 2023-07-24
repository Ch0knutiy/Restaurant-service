from schemas import schemas
from models import models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from database import get_db

router = APIRouter()


@router.get("/")
async def get_menus(db: Session = Depends(get_db)):
    return db.query(models.Menu).all()


@router.get("/{id}")
async def get_menu(id, db: Session = Depends(get_db)):
    menu = db.query(models.Menu).filter(models.Menu.id == id).first()
    if not menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"menu not found")
    return menu


@router.post("/", status_code=201)
def create_menu(payload: schemas.MenuSchema, db: Session = Depends(get_db)):
    menu = models.Menu(**payload.model_dump())
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return menu


@router.patch("/{id}", status_code=200)
async def update_menu(id, payload: schemas.MenuSchema, db: Session = Depends(get_db)):
    menu_query = db.query(models.Menu).filter(models.Menu.id == id)
    db_menu = menu_query.first()

    if not db_menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No menu with this id: {id} found')
    update_data = payload.model_dump(exclude_unset=True)
    menu_query.filter(models.Menu.id == id).update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(db_menu)
    return db_menu


@router.delete("/{id}", status_code=200)
async def delete_menu(id, db: Session = Depends(get_db)):
    menu_query = db.query(models.Menu).filter(models.Menu.id == id)
    menu = menu_query.first()
    if not menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No menu with this id: {id} found')
    menu_query.delete(synchronize_session=False)
    db.commit()
    return {"ok": True}
