import json
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from models import models
from repositories import repositoryCache, submenuRepository
from schemas import schemas
from sqlalchemy.orm import Session


def enrich_submenu(submenu: models.Submenu, db: Session) -> schemas.EnrichedSubmenuSchema | None:
    if not submenu:
        return None
    external_data = {
        'id': submenu.id,
        'title': submenu.title,
        'description': submenu.description,
        'dishes_count': submenuRepository.dishes_count(submenu.id, db)
    }
    return schemas.EnrichedSubmenuSchema(**external_data)


def get_submenus(menu_id: UUID, db: Session) -> list[schemas.EnrichedSubmenuSchema]:
    result = repositoryCache.get_cache('submenus' + str(menu_id))
    if not result:
        result = []
        for submenu in submenuRepository.get_submenus(menu_id, db):
            result.append(enrich_submenu(submenu, db))
        repositoryCache.set_cache('submenus' + str(menu_id), json.dumps(jsonable_encoder(result)))
    else:
        result = json.loads(result)
    return result


def get_submenu(id: UUID, db: Session) -> schemas.EnrichedSubmenuSchema | None:
    result = repositoryCache.get_cache('submenu' + str(id))
    if not result:
        result = enrich_submenu(submenuRepository.get_submenu(id, db), db)
        repositoryCache.set_cache('submenu' + str(id), json.dumps(jsonable_encoder(result)))
    else:
        result = json.loads(result)
    return result


def create_submenu(payload: schemas.SubmenuSchema, menu_id: UUID, db: Session) -> models.Submenu:
    repositoryCache.del_cache('menus')
    repositoryCache.del_cache('menus' + str(menu_id))
    repositoryCache.del_cache('submenus' + str(menu_id))
    return submenuRepository.create_submenu(payload, menu_id, db)


def update_submenu(id: UUID, menu_id: UUID, payload: schemas.SubmenuSchema, db: Session) -> models.Submenu | None:
    repositoryCache.del_cache('submenus' + str(menu_id))
    repositoryCache.del_cache('submenu' + str(id))
    return submenuRepository.update_submenu(id, payload, db)


def delete_submenu(id: UUID, menu_id: UUID, db: Session) -> dict[str, bool]:
    repositoryCache.del_cache('submenus' + str(menu_id))
    repositoryCache.del_cache('submenu' + str(id))
    repositoryCache.del_cache('menus')
    repositoryCache.del_cache('menus' + str(menu_id))
    return submenuRepository.delete_submenu(id, db)
