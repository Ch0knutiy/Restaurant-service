import json
from uuid import UUID

from fastapi import BackgroundTasks
from fastapi.encoders import jsonable_encoder
from models import models
from redis.asyncio import Redis
from repositories import repositoryCache, submenuRepository
from schemas import schemas
from sqlalchemy.ext.asyncio import AsyncSession


async def clear_submenu_cache(rd: Redis, menu_id: UUID, id: UUID | None = None) -> None:
    await repositoryCache.del_cache('submenus' + str(menu_id), rd)
    if id:
        await repositoryCache.del_cache('submenu' + str(id), rd)


async def clear_menu_cache(rd: Redis, menu_id: UUID) -> None:
    await repositoryCache.del_cache('menus', rd)
    await repositoryCache.del_cache('menus' + str(menu_id), rd)


async def enrich_submenu(submenu: models.Submenu, db: AsyncSession) -> schemas.EnrichedSubmenuSchema | None:
    if not submenu:
        return None
    external_data = {
        'id': submenu.id,
        'title': submenu.title,
        'description': submenu.description,
        'dishes_count': await submenuRepository.dishes_count(submenu.id, db)
    }
    return schemas.EnrichedSubmenuSchema(**external_data)


async def get_submenus(menu_id: UUID, db: AsyncSession, rd: Redis) -> list[schemas.EnrichedSubmenuSchema]:
    result = await repositoryCache.get_cache('submenus' + str(menu_id), rd)
    if result:
        return json.loads(result)
    result = []
    for submenu in await submenuRepository.get_submenus(menu_id, db):
        result.append(await enrich_submenu(submenu, db))
    await repositoryCache.set_cache('submenus' + str(menu_id), json.dumps(jsonable_encoder(result)), rd)
    return result


async def get_submenu(id: UUID, db: AsyncSession, rd: Redis) -> schemas.EnrichedSubmenuSchema | None:
    result = await repositoryCache.get_cache('submenu' + str(id), rd)
    if result:
        return json.loads(result)
    result = await enrich_submenu(await submenuRepository.get_submenu(id, db), db)
    await repositoryCache.set_cache('submenu' + str(id), json.dumps(jsonable_encoder(result)), rd)
    return result


async def create_submenu(payload: schemas.SubmenuSchema, menu_id: UUID, background_tasks: BackgroundTasks,
                         db: AsyncSession, rd: Redis) -> models.Submenu:
    background_tasks.add_task(clear_menu_cache, rd, menu_id)
    background_tasks.add_task(clear_submenu_cache, rd, menu_id, None)
    return await submenuRepository.create_submenu(payload, menu_id, db)


async def update_submenu(id: UUID, menu_id: UUID, payload: schemas.SubmenuSchema, background_tasks: BackgroundTasks,
                         db: AsyncSession, rd: Redis) -> models.Submenu | None:
    background_tasks.add_task(clear_submenu_cache, rd, menu_id, id)
    return await submenuRepository.update_submenu(id, payload, db)


async def delete_submenu(id: UUID, menu_id: UUID, background_tasks: BackgroundTasks,
                         db: AsyncSession, rd: Redis) -> dict[str, bool]:
    background_tasks.add_task(clear_menu_cache, rd, menu_id)
    background_tasks.add_task(clear_submenu_cache, rd, menu_id, id)
    return await submenuRepository.delete_submenu(id, db)
