import json
from uuid import UUID

from fastapi import BackgroundTasks
from fastapi.encoders import jsonable_encoder
from models import models
from redis.asyncio import Redis
from repositories import menuRepository, repositoryCache
from schemas import schemas
from sqlalchemy.ext.asyncio import AsyncSession


async def clear_menu_cache(rd: Redis, id: UUID | None = None) -> None:
    await repositoryCache.del_cache('menus', rd)
    if id:
        await repositoryCache.del_cache('menus' + str(id), rd)


async def enrich_menu(menu: models.Menu, db: AsyncSession) -> schemas.EnrichedMenuSchema | None:
    if not menu:
        return None
    data_to_add = await menuRepository.menu_counts(menu.id, db)
    external_data = {
        'id': menu.id,
        'title': menu.title,
        'description': menu.description,
        'submenus_count': data_to_add[0],
        'dishes_count': data_to_add[1]
    }
    return schemas.EnrichedMenuSchema(**external_data)


async def get_menus(db: AsyncSession, rd: Redis) -> list[schemas.EnrichedMenuSchema]:
    result = await repositoryCache.get_cache('menus', rd)
    if result:
        return json.loads(result)
    result = []
    for menu in await menuRepository.get_menus(db):
        result.append(await enrich_menu(menu, db))
    await repositoryCache.set_cache('menus', json.dumps(jsonable_encoder(result)), rd)
    return result


async def get_menu(id: UUID, db: AsyncSession, rd: Redis) -> schemas.EnrichedMenuSchema | None:
    result = await repositoryCache.get_cache('menus' + str(id), rd)
    if result:
        return json.loads(result)
    result = await enrich_menu(await menuRepository.get_menu(id, db), db)
    await repositoryCache.set_cache('menus' + str(id), json.dumps(jsonable_encoder(result)), rd)
    return result


async def create_menu(payload: schemas.MenuSchema, background_tasks: BackgroundTasks,
                      db: AsyncSession, rd: Redis) -> models.Menu:
    background_tasks.add_task(clear_menu_cache, rd, None)
    return await menuRepository.create_menu(payload, db)


async def update_menu(id: UUID, payload: schemas.MenuSchema, background_tasks: BackgroundTasks,
                      db: AsyncSession, rd: Redis) -> models.Menu | None:
    background_tasks.add_task(clear_menu_cache, rd, id)
    return await menuRepository.update_menu(id, payload, db)


async def delete_menu(id: UUID, background_tasks: BackgroundTasks, db: AsyncSession, rd: Redis) -> dict[str, bool]:
    background_tasks.add_task(clear_menu_cache, rd, id)
    return await menuRepository.delete_menu(id, db)
