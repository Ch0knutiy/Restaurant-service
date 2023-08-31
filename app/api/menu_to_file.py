from database import get_session
from fastapi import APIRouter, Depends
from redis.asyncio import Redis
from redis_connection import get_redis
from schemas import schemas
from services import menuService
from sqlalchemy.ext.asyncio import AsyncSession
from tasks.tasks import get_xlsx_full_menu

router = APIRouter()


@router.get('/full_file', response_model=schemas.Delete)
async def get_xlsx_menus(db: AsyncSession = Depends(get_session), rd: Redis = Depends(get_redis)):
    menus_to_file = await menuService.get_menus_full(db, rd)
    if not menus_to_file:
        return {'ok': False}
    get_xlsx_full_menu.delay(menus_to_file)
    return {'ok': True}
