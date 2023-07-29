from repositories import dishRepository


def get_dishes(submenu_id, db):
    return dishRepository.get_dishes(submenu_id, db)


def get_dish(id, db):
    return dishRepository.get_dish(id, db)


def create_dish(payload, submenu_id, db):
    return dishRepository.create_dish(payload, submenu_id, db)


def update_dish(id, payload, db):
    return dishRepository.update_dish(id, payload, db)


def delete_dish(id, db):
    return dishRepository.delete_dish(id, db)
