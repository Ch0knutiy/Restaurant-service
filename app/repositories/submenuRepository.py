from uuid import UUID

from models import models
from schemas import schemas
from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession


async def dishes_count(id: UUID, db: AsyncSession) -> int:
    sub_select = select(models.Dish.id).filter(models.Dish.submenu_id == id)
    result = await db.execute(select(func.count()).select_from(sub_select))
    return result.scalars().first()


async def get_submenus(menu_id: UUID, db: AsyncSession) -> list[models.Submenu]:
    result = await db.execute(select(models.Submenu).filter(models.Submenu.menu_id == menu_id))
    return list[models.Submenu](result.scalars().all())


async def get_submenu(id: UUID, db: AsyncSession) -> models.Submenu | None:
    result = await db.execute(select(models.Submenu).filter(models.Submenu.id == id))
    return result.scalars().first()


async def create_submenu(payload: schemas.SubmenuSchema, menu_id: UUID, db: AsyncSession) -> models.Submenu:
    submenu = models.Submenu(**payload.model_dump(), menu_id=menu_id)
    db.add(submenu)
    await db.commit()
    return submenu


async def update_submenu(id: UUID, payload: schemas.SubmenuSchema, db: AsyncSession) -> models.Submenu | None:
    query = await db.execute(update(models.Submenu).
                             where(models.Submenu.id == id).
                             values(payload.model_dump(exclude_unset=True)).
                             returning(models.Submenu))
    submenu = query.scalars().first()
    await db.commit()
    return submenu


async def delete_submenu(id: UUID, db: AsyncSession) -> dict[str, bool]:
    query = await db.execute(delete(models.Submenu).where(models.Submenu.id == id).returning(models.Submenu))
    submenu = query.scalars().first()
    if not submenu:
        return {'ok': False}
    await db.commit()
    return {'ok': True}
