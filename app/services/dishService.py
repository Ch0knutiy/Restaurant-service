import json
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from models import models
from repositories import dishRepository, repositoryCache
from schemas import schemas
from sqlalchemy.orm import Session


def get_dishes(submenu_id: UUID, db: Session) -> list[models.Dish]:
    result = repositoryCache.get_cache('dishes' + str(submenu_id))
    if not result:
        result = dishRepository.get_dishes(submenu_id, db)
        repositoryCache.set_cache('dishes' + str(submenu_id), json.dumps(jsonable_encoder(result)))
    else:
        result = json.loads(result)
    return result


def get_dish(id: UUID, db: Session) -> models.Dish | None:
    result = repositoryCache.get_cache('dish' + str(id))
    if not result:
        result = dishRepository.get_dish(id, db)
        repositoryCache.set_cache('dish' + str(id), json.dumps(jsonable_encoder(result)))
    else:
        result = json.loads(result)
    return result


def create_dish(payload: schemas.DishSchema, submenu_id: UUID, menu_id: UUID, db: Session) -> models.Dish:
    repositoryCache.del_cache('dishes' + str(submenu_id))
    repositoryCache.del_cache('submenus' + str(menu_id))
    repositoryCache.del_cache('submenu' + str(submenu_id))
    repositoryCache.del_cache('menus')
    repositoryCache.del_cache('menus' + str(menu_id))
    return dishRepository.create_dish(payload, submenu_id, db)


def update_dish(id: UUID, submenu_id: UUID, payload: schemas.DishSchema, db: Session) -> models.Dish | None:
    repositoryCache.del_cache('dishes' + str(submenu_id))
    repositoryCache.del_cache('dish' + str(id))
    return dishRepository.update_dish(id, payload, db)


def delete_dish(id: UUID, submenu_id: UUID, menu_id: UUID, db: Session) -> dict[str, bool]:
    repositoryCache.del_cache('dishes' + str(submenu_id))
    repositoryCache.del_cache('dish' + str(id))
    repositoryCache.del_cache('submenus' + str(menu_id))
    repositoryCache.del_cache('submenu' + str(submenu_id))
    repositoryCache.del_cache('menus')
    repositoryCache.del_cache('menus' + str(menu_id))
    return dishRepository.delete_dish(id, db)
