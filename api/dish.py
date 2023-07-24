from schemas import schemas
from models import models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from database import get_db


router = APIRouter()


@router.get("/{menu_id}/submenus/{submenu_id}/dishes")
async def get_dishes(submenu_id, db: Session = Depends(get_db)):
    return db.query(models.Dish).filter(models.Dish.submenu_id == submenu_id).all()


@router.get("/{menu_id}/submenus/{submenu_id}/dishes/{id}")
async def get_dish(id, db: Session = Depends(get_db)):
    dish = db.query(models.Dish).filter(models.Dish.id == id).first()
    if not dish:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"dish not found")
    return dish


@router.post("/{menu_id}/submenus/{submenu_id}/dishes", status_code=201)
def create_dish(payload: schemas.DishSchema, menu_id, submenu_id, db: Session = Depends(get_db)):
    dish = models.Dish(**payload.model_dump(), submenu_id=submenu_id)
    menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    menu.dishes_count += 1
    submenu = db.query(models.Submenu).filter(models.Submenu.id == submenu_id).first()
    submenu.dishes_count += 1
    db.add(dish)
    db.commit()
    db.refresh(dish)
    return dish


@router.patch("/{menu_id}/submenus/{submenu_id}/dishes/{id}", status_code=200)
async def update_dish(id, payload: schemas.DishSchema, db: Session = Depends(get_db)):
    dish_query = db.query(models.Dish).filter(models.Dish.id == id)
    db_dish = dish_query.first()

    if not db_dish:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No submenu with this id: {id} found')
    update_data = payload.model_dump(exclude_unset=True)
    dish_query.filter(models.Dish.id == id).update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(db_dish)
    return db_dish


@router.delete("/{menu_id}/submenus/{submenu_id}/dishes/{id}", status_code=200)
async def delete_dish(id, submenu_id, menu_id, db: Session = Depends(get_db)):
    dish_query = db.query(models.Dish).filter(models.Dish.id == id)
    dish = dish_query.first()
    if not dish:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No submenu with this id: {id} found')
    menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    menu.dishes_count -= 1
    submenu = db.query(models.Submenu).filter(models.Submenu.id == submenu_id).first()
    submenu.dishes_count -= 1
    dish_query.delete(synchronize_session=False)
    db.commit()
    return {"ok": True}
