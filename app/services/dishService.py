import json
from uuid import UUID

from fastapi import BackgroundTasks
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


async def get_dishes(submenu_id: UUID, db: Session) -> list[models.Dish]:
    result = repositoryCache.get_cache('dishes' + str(submenu_id))
    if result:
        return json.loads(result)
    result = await dishRepository.get_dishes(submenu_id, db)
    repositoryCache.set_cache('dishes' + str(submenu_id), json.dumps(jsonable_encoder(result)))
    return result


async def get_dish(id: UUID, db: Session) -> models.Dish | None:
    result = repositoryCache.get_cache('dish' + str(id))
    if result:
        return json.loads(result)
    result = await dishRepository.get_dish(id, db)
    repositoryCache.set_cache('dish' + str(id), json.dumps(jsonable_encoder(result)))
    return result


async def create_dish(payload: schemas.DishSchema, submenu_id: UUID, menu_id: UUID, background_tasks: BackgroundTasks,
                      db: Session) -> models.Dish:
    background_tasks.add_task(clear_dish_cache, submenu_id, None)
    background_tasks.add_task(clear_upper_cache, menu_id, submenu_id)
    return await dishRepository.create_dish(payload, submenu_id, db)


async def update_dish(id: UUID, submenu_id: UUID, payload: schemas.DishSchema, background_tasks: BackgroundTasks,
                      db: Session) -> models.Dish | None:
    background_tasks.add_task(clear_dish_cache, submenu_id, id)
    return await dishRepository.update_dish(id, payload, db)


async def delete_dish(id: UUID, submenu_id: UUID, menu_id: UUID, background_tasks: BackgroundTasks,
                      db: Session) -> dict[str, bool]:
    background_tasks.add_task(clear_dish_cache, submenu_id, id)
    background_tasks.add_task(clear_upper_cache, menu_id, submenu_id)
    return await dishRepository.delete_dish(id, db)
