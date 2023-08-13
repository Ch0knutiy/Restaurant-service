from uuid import UUID

from models import models
from schemas import schemas
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession


async def get_dishes(submenu_id: UUID, db: AsyncSession) -> list[models.Dish]:
    result = await db.execute(select(models.Dish).filter(models.Dish.submenu_id == submenu_id))
    return list[models.Dish](result.scalars().all())


async def get_dish(id: UUID, db: AsyncSession) -> models.Dish:
    result = await db.execute(select(models.Dish).filter(models.Dish.id == id))
    return result.scalars().first()


async def create_dish(payload: schemas.DishSchema, submenu_id: UUID, db: AsyncSession) -> models.Dish:
    dish = models.Dish(**payload.model_dump(), submenu_id=submenu_id)
    db.add(dish)
    await db.commit()
    return dish


async def update_dish(id: UUID, payload: schemas.DishSchema, db: AsyncSession) -> models.Dish | None:
    query = await db.execute(update(models.Dish).
                             where(models.Dish.id == id).
                             values(payload.model_dump(exclude_unset=True)).
                             returning(models.Dish))
    dish = query.scalars().first()
    await db.commit()
    return dish


async def delete_dish(id: UUID, db: AsyncSession) -> dict[str, bool]:
    query = await db.execute(delete(models.Dish).where(models.Dish.id == id).returning(models.Dish))
    dish = query.scalars().first()
    if not dish:
        return {'ok': False}
    await db.commit()
    return {'ok': True}
