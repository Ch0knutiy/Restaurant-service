import json
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from models import models
from repositories import menuRepository, repositoryCache
from schemas import schemas
from sqlalchemy.orm import Session


def enrich_menu(menu: models.Menu, db: Session) -> schemas.EnrichedMenuSchema | None:
    if not menu:
        return None
    external_data = {
        'id': menu.id,
        'title': menu.title,
        'description': menu.description,
        'submenus_count': menuRepository.submenus_count(menu.id, db),
        'dishes_count': menuRepository.dishes_count(menu.id, db)
    }
    return schemas.EnrichedMenuSchema(**external_data)


def get_menus(db: Session) -> list[schemas.EnrichedMenuSchema]:
    result = repositoryCache.get_cache('menus')
    if not result:
        result = []
        for menu in menuRepository.get_menus(db):
            result.append(enrich_menu(menu, db))
        repositoryCache.set_cache('menus', json.dumps(jsonable_encoder(result)))
    else:
        result = json.loads(result)
    return result


def get_menu(id: UUID, db: Session) -> schemas.EnrichedMenuSchema | None:
    result = repositoryCache.get_cache('menus' + str(id))
    if not result:
        result = enrich_menu(menuRepository.get_menu(id, db), db)
        repositoryCache.set_cache('menus', json.dumps(jsonable_encoder(result)))
    else:
        result = json.loads(result)
    return result


def create_menu(payload: schemas.MenuSchema, db: Session) -> models.Menu:
    repositoryCache.del_cache('menus')
    return menuRepository.create_menu(payload, db)


def update_menu(id: UUID, payload: schemas.MenuSchema, db: Session) -> models.Menu | None:
    repositoryCache.del_cache('menus')
    repositoryCache.del_cache('menus' + str(id))
    return menuRepository.update_menu(id, payload, db)


def delete_menu(id: UUID, db: Session) -> dict[str, bool]:
    repositoryCache.del_cache('menus')
    repositoryCache.del_cache('menus' + str(id))
    return menuRepository.delete_menu(id, db)
