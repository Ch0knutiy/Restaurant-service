from repositories import submenuRepository
from schemas import schemas


def enrich_submenu(submenu, db):
    if not submenu:
        return None
    external_data = {
        'id': submenu.id,
        'title': submenu.title,
        'description': submenu.description,
        'dishes_count': submenuRepository.dishes_count(submenu.id, db)
    }
    return schemas.EnrichedSubmenuSchema(**external_data)


def get_submenus(menu_id, db):
    result = []
    for submenu in submenuRepository.get_submenus(menu_id, db):
        result.append(enrich_submenu(submenu, db))
    return result


def get_submenu(id, db):
    return enrich_submenu(submenuRepository.get_submenu(id, db), db)


def create_submenu(payload, menu_id, db):
    return submenuRepository.create_submenu(payload, menu_id, db)


def update_submenu(id, payload, db):
    return submenuRepository.update_submenu(id, payload, db)


def delete_submenu(id, db):
    return submenuRepository.delete_submenu(id, db)
