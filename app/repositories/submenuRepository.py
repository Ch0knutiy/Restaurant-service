from uuid import UUID

from models import models
from schemas import schemas
from sqlalchemy.orm import Session


def dishes_count(id: UUID, db: Session) -> int:
    return db.query(models.Dish.id).filter(models.Dish.submenu_id == id).count()


def get_submenus(menu_id: UUID, db: Session) -> list[models.Submenu]:
    return db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id).all()


def get_submenu(id: UUID, db: Session) -> models.Submenu:
    return db.query(models.Submenu).filter(models.Submenu.id == id).first()


def create_submenu(payload: schemas.SubmenuSchema, menu_id: UUID, db: Session) -> models.Submenu:
    submenu = models.Submenu(**payload.model_dump(), menu_id=menu_id)
    db.add(submenu)
    db.commit()
    db.refresh(submenu)
    return submenu


def update_submenu(id: UUID, payload: schemas.SubmenuSchema, db: Session) -> models.Submenu | None:
    query = db.query(models.Submenu).filter(models.Submenu.id == id)
    submenu = query.first()
    if not submenu:
        return None
    update_data = payload.model_dump(exclude_unset=True)
    query.filter(models.Submenu.id == id).update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(submenu)
    return submenu


def delete_submenu(id: UUID, db: Session) -> dict[str, bool]:
    query = db.query(models.Submenu).filter(models.Submenu.id == id)
    submenu = query.first()
    if not submenu:
        return {'ok': False}
    query.delete(synchronize_session=False)
    db.commit()
    return {'ok': True}
