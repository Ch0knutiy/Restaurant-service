import json
from uuid import UUID

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
    if not result:
        result = []
        for submenu in submenuRepository.get_submenus(menu_id, db):
            result.append(enrich_submenu(submenu, db))
        repositoryCache.set_cache('submenus' + str(menu_id), json.dumps(jsonable_encoder(result)))
    else:
        result = json.loads(result)
    return result


async def get_submenu(id: UUID, db: Session) -> schemas.EnrichedSubmenuSchema | None:
    result = repositoryCache.get_cache('submenu' + str(id))
    if not result:
        result = enrich_submenu(submenuRepository.get_submenu(id, db), db)
        repositoryCache.set_cache('submenu' + str(id), json.dumps(jsonable_encoder(result)))
    else:
        result = json.loads(result)
    return result


async def create_submenu(payload: schemas.SubmenuSchema, menu_id: UUID, db: Session) -> models.Submenu:
    clear_menu_cache(menu_id)
    clear_submenu_cache(menu_id)
    return submenuRepository.create_submenu(payload, menu_id, db)


async def update_submenu(id: UUID, menu_id: UUID, payload: schemas.SubmenuSchema, db: Session) -> models.Submenu | None:
    clear_submenu_cache(menu_id, id)
    return submenuRepository.update_submenu(id, payload, db)


async def delete_submenu(id: UUID, menu_id: UUID, db: Session) -> dict[str, bool]:
    clear_submenu_cache(menu_id, id)
    clear_menu_cache(menu_id)
    return submenuRepository.delete_submenu(id, db)
