from sqlalchemy.orm import Session

from app.models.building import Building
from app.services.base import CRUDBase


class CRUDBuilding(CRUDBase):
    """CRUD для зданий."""

    def get_by_bounding_box(
        self,
        db: Session,
        min_lat: float,
        max_lat: float,
        min_lon: float,
        max_lon: float
    ) -> list[Building]:
        """Получить здания внутри прямоугольной области по координатам."""
        return db.query(Building).filter(
            Building.latitude.between(min_lat, max_lat),
            Building.longitude.between(min_lon, max_lon)
        ).all()


crud_building = CRUDBuilding(Building)
