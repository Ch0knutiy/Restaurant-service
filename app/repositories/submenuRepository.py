from models import models
from schemas import schemas


def dishes_count(id, db):
    return db.query(models.Dish.id).filter(models.Dish.submenu_id == id).count()


def get_submenus(menu_id, db):
    return db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id).all()


def get_submenu(id, db):
    return db.query(models.Submenu).filter(models.Submenu.id == id).first()


def create_submenu(payload: schemas.SubmenuSchema, menu_id, db):
    submenu = models.Submenu(**payload.model_dump(), menu_id=menu_id)
    db.add(submenu)
    db.commit()
    db.refresh(submenu)
    return submenu


def update_submenu(id, payload: schemas.SubmenuSchema, db):
    query = db.query(models.Submenu).filter(models.Submenu.id == id)
    submenu = query.first()
    if not submenu:
        return None
    update_data = payload.model_dump(exclude_unset=True)
    query.filter(models.Submenu.id == id).update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(submenu)
    return submenu


def delete_submenu(id, db):
    query = db.query(models.Submenu).filter(models.Submenu.id == id)
    submenu = query.first()
    if not submenu:
        return {"ok": False}
    query.delete(synchronize_session=False)
    db.commit()
    return {"ok": True}
