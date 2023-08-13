import json
from uuid import UUID

from fastapi import BackgroundTasks
from fastapi.encoders import jsonable_encoder
from models import models
from redis.asyncio import Redis
from repositories import dishRepository, repositoryCache
from schemas import schemas
from sqlalchemy.ext.asyncio import AsyncSession


async def clear_upper_cache(rd: Redis, menu_id: UUID, submenu_id: UUID):
    await repositoryCache.del_cache('submenus' + str(menu_id), rd)
    await repositoryCache.del_cache('submenu' + str(submenu_id), rd)
    await repositoryCache.del_cache('menus', rd)
    await repositoryCache.del_cache('menus' + str(menu_id), rd)


async def clear_dish_cache(rd: Redis, submenu_id: UUID, id: UUID | None = None) -> None:
    await repositoryCache.del_cache('dishes' + str(submenu_id), rd)
    if id:
        await repositoryCache.del_cache('dish' + str(id), rd)


async def get_dishes(submenu_id: UUID, db: AsyncSession, rd: Redis) -> list[models.Dish]:
    result = await repositoryCache.get_cache('dishes' + str(submenu_id), rd)
    if result:
        return json.loads(result)
    result = await dishRepository.get_dishes(submenu_id, db)
    await repositoryCache.set_cache('dishes' + str(submenu_id), json.dumps(jsonable_encoder(result)), rd)
    return result


async def get_dish(id: UUID, db: AsyncSession, rd: Redis) -> models.Dish | None:
    result = await repositoryCache.get_cache('dish' + str(id), rd)
    if result:
        return json.loads(result)
    result = await dishRepository.get_dish(id, db)
    await repositoryCache.set_cache('dish' + str(id), json.dumps(jsonable_encoder(result)), rd)
    return result


async def create_dish(payload: schemas.DishSchema, submenu_id: UUID, menu_id: UUID, background_tasks: BackgroundTasks,
                      db: AsyncSession, rd: Redis) -> models.Dish:
    background_tasks.add_task(clear_dish_cache, rd, submenu_id, None)
    background_tasks.add_task(clear_upper_cache, rd, menu_id, submenu_id)
    return await dishRepository.create_dish(payload, submenu_id, db)


async def update_dish(id: UUID, submenu_id: UUID, payload: schemas.DishSchema, background_tasks: BackgroundTasks,
                      db: AsyncSession, rd: Redis) -> models.Dish | None:
    background_tasks.add_task(clear_dish_cache, rd, submenu_id, id)
    return await dishRepository.update_dish(id, payload, db)


async def delete_dish(id: UUID, submenu_id: UUID, menu_id: UUID, background_tasks: BackgroundTasks,
                      db: AsyncSession, rd: Redis) -> dict[str, bool]:
    background_tasks.add_task(clear_dish_cache, rd, submenu_id, id)
    background_tasks.add_task(clear_upper_cache, rd, menu_id, submenu_id)
    return await dishRepository.delete_dish(id, db)
