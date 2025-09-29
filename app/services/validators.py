from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Organization, Building, Activity


async def check_organization_exists(
    db: AsyncSession, organization_id: int
) -> Organization:
    result = await db.execute(select(Organization).where(Organization.id == organization_id))
    org = result.scalars().first()
    if org is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Организация не найдена"
        )
    return org


async def check_organization_name_duplicate(db: AsyncSession, name: str) -> None:
    result = await db.execute(select(Organization).where(Organization.name == name))
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Организация с таким названием уже существует"
        )


async def check_building_exists(db: AsyncSession, building_id: int) -> Building:
    result = await db.execute(select(Building).where(Building.id == building_id))
    building = result.scalars().first()
    if building is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Здание не найдено"
        )
    return building


async def check_building_address_duplicate(db: AsyncSession, address: str) -> None:
    result = await db.execute(select(Building).where(Building.address == address))
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Здание с таким адресом уже существует"
        )


async def check_activity_exists(db: AsyncSession, activity_id: int) -> Activity:
    result = await db.execute(select(Activity).where(Activity.id == activity_id))
    activity = result.scalars().first()
    if activity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вид деятельности не найден"
        )
    return activity


async def check_activity_name_duplicate(db: AsyncSession, name: str) -> None:
    result = await db.execute(select(Activity).where(Activity.name == name))
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Вид деятельности с таким названием уже существует"
        )


def check_activity_level_limit(activity: Activity) -> None:
    """Не более 3 уровней вложенности"""
    level = 0
    current = activity
    while current.parent is not None:
        level += 1
        if level >= 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Превышен допустимый уровень вложенности (максимум 3)"
            )
        current = current.parent
