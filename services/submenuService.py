from repositories import submenuRepository


def get_submenus(menu_id, db):
    return submenuRepository.get_submenus(menu_id, db)


def get_submenu(id, db):
    return submenuRepository.get_submenu(id, db)


def create_submenu(payload, menu_id, db):
    return submenuRepository.create_submenu(payload, menu_id, db)


def update_submenu(id, payload, db):
    return submenuRepository.update_submenu(id, payload, db)


def delete_submenu(id, db):
    return submenuRepository.delete_submenu(id, db)
