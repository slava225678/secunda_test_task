from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.building import Building
from app.services.base import CRUDBase


class CRUDBuilding(CRUDBase):
    """CRUD для зданий (асинхронный)."""

    async def get_by_bounding_box(
        self,
        db: AsyncSession,
        min_lat: float,
        max_lat: float,
        min_lon: float,
        max_lon: float
    ) -> list[Building]:
        """Получить здания внутри прямоугольной области по координатам."""
        result = await db.execute(
            select(Building).where(
                Building.latitude.between(min_lat, max_lat),
                Building.longitude.between(min_lon, max_lon)
            )
        )
        return result.scalars().all()


crud_building = CRUDBuilding(Building)
