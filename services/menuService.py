from repositories import menuRepository
from schemas import schemas


def enrich_menu(menu, db):
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


def get_menus(db):
    result = []
    for menu in menuRepository.get_menus(db):
        result.append(enrich_menu(menu, db))
    return result


def get_menu(id, db):
    return enrich_menu(menuRepository.get_menu(id, db), db)


def create_menu(payload, db):
    return menuRepository.create_menu(payload, db)


def update_menu(id, payload, db):
    return menuRepository.update_menu(id, payload, db)


def delete_menu(id, db):
    return menuRepository.delete_menu(id, db)
