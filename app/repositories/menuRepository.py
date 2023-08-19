from uuid import UUID

from models import models
from schemas import schemas
from sqlalchemy import delete, func, select, union_all, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


async def get_menus_full(db: AsyncSession) -> list[models.Menu]:
    result = await db.execute(select(models.Menu).
                              options(selectinload(models.Menu.submenus).selectinload(models.Submenu.dishes)))
    return list[models.Menu](result.scalars().all())


async def menu_counts(id: UUID, db: AsyncSession) -> list[int]:
    sub_select_for_submenu = select(models.Submenu.id).filter(models.Submenu.menu_id == id)
    sub_select_for_dishes = select(models.Dish.id).join(models.Submenu).\
        where(models.Submenu.menu_id == id, models.Submenu.id == models.Dish.submenu_id)
    result = await db.execute(union_all(select(func.count()).select_from(sub_select_for_submenu),
                                        select(func.count()).select_from(sub_select_for_dishes)))
    return list[int](result.scalars().all())


async def get_menus(db: AsyncSession) -> list[models.Menu]:
    result = await db.execute(select(models.Menu))
    return list[models.Menu](result.scalars().all())


async def get_menu(id: UUID, db: AsyncSession) -> models.Menu | None:
    result = await db.execute(select(models.Menu).filter(models.Menu.id == id))
    return result.scalars().first()


async def create_menu(payload: schemas.MenuSchema, db: AsyncSession) -> models.Menu:
    menu = models.Menu(**payload.model_dump())
    db.add(menu)
    await db.commit()
    return menu


async def update_menu(id: UUID, payload: schemas.MenuSchema, db: AsyncSession) -> models.Menu | None:
    query = await db.execute(update(models.Menu).
                             where(models.Menu.id == id).
                             values(payload.model_dump(exclude_unset=True)).
                             returning(models.Menu))
    menu = query.scalars().first()
    await db.commit()
    return menu


async def delete_menu(id: UUID, db: AsyncSession) -> dict[str, bool]:
    query = await db.execute(delete(models.Menu).where(models.Menu.id == id).returning(models.Menu))
    menu = query.scalars().first()
    if not menu:
        return {'ok': False}
    await db.commit()
    return {'ok': True}
