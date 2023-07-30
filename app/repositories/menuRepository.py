from models import models
from schemas import schemas


def get_menus(db):
    return db.query(models.Menu).all()


def get_menu(id, db):
    return db.query(models.Menu).filter(models.Menu.id == id).first()


def create_menu(payload: schemas.MenuSchema, db):
    menu = models.Menu(**payload.model_dump())
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return menu


def update_menu(id, payload: schemas.MenuSchema, db):
    query = db.query(models.Menu).filter(models.Menu.id == id)
    menu = query.first()
    if not menu:
        return None
    update_data = payload.model_dump(exclude_unset=True)
    query.filter(models.Menu.id == id).update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(menu)
    return menu


def delete_menu(id, db):
    query = db.query(models.Menu).filter(models.Menu.id == id)
    menu = query.first()
    if not menu:
        return {"ok": False}
    query.delete(synchronize_session=False)
    db.commit()
    return {"ok": True}


def submenus_count(id, db):
    return db.query(models.Submenu.id).filter(models.Submenu.menu_id == id).count()


def dishes_count(id, db):
    return db.query(models.Dish.id).join(models.Submenu).where(models.Submenu.menu_id == id, models.Submenu.id ==
                                                               models.Dish.submenu_id).count()
