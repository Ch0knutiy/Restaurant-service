import json
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from models import models
from repositories import dishRepository, repositoryCache
from schemas import schemas
from sqlalchemy.orm import Session


def clear_upper_cache(menu_id: UUID, submenu_id: UUID) -> None:
    repositoryCache.del_cache('submenus' + str(menu_id))
    repositoryCache.del_cache('submenu' + str(submenu_id))
    repositoryCache.del_cache('menus')
    repositoryCache.del_cache('menus' + str(menu_id))


def clear_dish_cache(submenu_id: UUID, id: UUID | None = None) -> None:
    repositoryCache.del_cache('dishes' + str(submenu_id))
    if id:
        repositoryCache.del_cache('dish' + str(id))


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
    clear_dish_cache(submenu_id)
    clear_upper_cache(menu_id, submenu_id)
    return dishRepository.create_dish(payload, submenu_id, db)


def update_dish(id: UUID, submenu_id: UUID, payload: schemas.DishSchema, db: Session) -> models.Dish | None:
    clear_dish_cache(submenu_id, id)
    return dishRepository.update_dish(id, payload, db)


def delete_dish(id: UUID, submenu_id: UUID, menu_id: UUID, db: Session) -> dict[str, bool]:
    clear_dish_cache(submenu_id, id)
    clear_upper_cache(menu_id, submenu_id)
    return dishRepository.delete_dish(id, db)
