import json
from uuid import UUID

from fastapi import BackgroundTasks
from fastapi.encoders import jsonable_encoder
from models import models
from repositories import repositoryCache, submenuRepository
from schemas import schemas
from sqlalchemy.orm import Session


def clear_submenu_cache(menu_id: UUID, id: UUID | None = None) -> None:
    repositoryCache.del_cache('submenus' + str(menu_id))
    if id:
        repositoryCache.del_cache('submenu' + str(id))


def clear_menu_cache(menu_id: UUID) -> None:
    repositoryCache.del_cache('menus')
    repositoryCache.del_cache('menus' + str(menu_id))


async def enrich_submenu(submenu: models.Submenu, db: Session) -> schemas.EnrichedSubmenuSchema | None:
    if not submenu:
        return None
    external_data = {
        'id': submenu.id,
        'title': submenu.title,
        'description': submenu.description,
        'dishes_count': await submenuRepository.dishes_count(submenu.id, db)
    }
    return schemas.EnrichedSubmenuSchema(**external_data)


async def get_submenus(menu_id: UUID, db: Session) -> list[schemas.EnrichedSubmenuSchema]:
    result = repositoryCache.get_cache('submenus' + str(menu_id))
    if result:
        return json.loads(result)
    result = []
    for submenu in await submenuRepository.get_submenus(menu_id, db):
        result.append(await enrich_submenu(submenu, db))
    repositoryCache.set_cache('submenus' + str(menu_id), json.dumps(jsonable_encoder(result)))
    return result


async def get_submenu(id: UUID, db: Session) -> schemas.EnrichedSubmenuSchema | None:
    result = repositoryCache.get_cache('submenu' + str(id))
    if result:
        return json.loads(result)
    result = await enrich_submenu(await submenuRepository.get_submenu(id, db), db)
    repositoryCache.set_cache('submenu' + str(id), json.dumps(jsonable_encoder(result)))
    return result


async def create_submenu(payload: schemas.SubmenuSchema, menu_id: UUID, background_tasks: BackgroundTasks,
                         db: Session) -> models.Submenu:
    background_tasks.add_task(clear_menu_cache, menu_id)
    background_tasks.add_task(clear_submenu_cache, menu_id, None)
    return await submenuRepository.create_submenu(payload, menu_id, db)


async def update_submenu(id: UUID, menu_id: UUID, payload: schemas.SubmenuSchema, background_tasks: BackgroundTasks,
                         db: Session) -> models.Submenu | None:
    background_tasks.add_task(clear_submenu_cache, menu_id, id)
    return await submenuRepository.update_submenu(id, payload, db)


async def delete_submenu(id: UUID, menu_id: UUID, background_tasks: BackgroundTasks,
                         db: Session) -> dict[str, bool]:
    background_tasks.add_task(clear_menu_cache, menu_id)
    background_tasks.add_task(clear_submenu_cache, menu_id, id)
    return await submenuRepository.delete_submenu(id, db)
