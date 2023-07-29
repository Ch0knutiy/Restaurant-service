from repositories import menuRepository


def get_menus(db):
    return menuRepository.get_menus(db)


def get_menu(id, db):
    return menuRepository.get_menu(id, db)


def create_menu(payload, db):
    return menuRepository.create_menu(payload, db)


def update_menu(id, payload, db):
    return menuRepository.update_menu(id, payload, db)


def delete_menu(id, db):
    return menuRepository.delete_menu(id, db)
