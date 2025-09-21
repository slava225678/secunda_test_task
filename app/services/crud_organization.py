from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas.organization import OrganizationCreate
from app.services.base import CRUDBase
from app.models import Organization, OrganizationPhone
from app.models.activity import Activity


class CRUDOrganization(CRUDBase):
    """CRUD для организаций с поддержкой телефонов и видов деятельности."""

    def create_organization(
        self,
        db: Session,
        obj_in: OrganizationCreate
    ) -> Organization:
        """
        Создание организации с телефонами и
        привязкой к видам деятельности.
        """
        org_data = obj_in.model_dump(exclude={"phones", "activity_ids"})
        org = Organization(**org_data)

        # привязка к видам деятельности
        if obj_in.activity_ids:
            activities = db.query(
                Activity
            ).filter(Activity.id.in_(obj_in.activity_ids)).all()
            if len(activities) != len(obj_in.activity_ids):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Некоторые виды деятельности не найдены."
                )
            org.activities = activities

        db.add(org)
        db.commit()
        db.refresh(org)

        # добавление телефонов
        for phone in obj_in.phones or []:
            org_phone = OrganizationPhone(phone_number=phone, organization=org)
            db.add(org_phone)

        db.commit()
        db.refresh(org)
        return org

    def get_by_building(
            self, db: Session, building_id: int
    ) -> list[Organization]:
        """Получить все организации в конкретном здании."""
        return db.query(
            Organization
        ).filter(Organization.building_id == building_id).all()

    def get_by_buildings(
        self, db: Session, building_ids: list[int]
    ) -> list[Organization]:
        """Получить организации по списку зданий."""
        return db.query(Organization).filter(
            Organization.building_id.in_(building_ids)
        ).all()

    def get_by_activity(
            self, db: Session, activity_id: int
    ) -> list[Organization]:
        """
        Получить все организации по виду деятельности,
        включая вложенные до 3 уровня.
        """
        activity = db.query(
            Activity
        ).filter(Activity.id == activity_id).first()
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")

        # собираем id всех вложенных активностей (до 3 уровня)
        def collect_ids(act: Activity, level=1, max_level=3):
            ids = [act.id]
            if level < max_level:
                for child in act.children:
                    ids.extend(collect_ids(child, level + 1, max_level))
            return ids

        activity_ids = collect_ids(activity)

        return (
            db.query(Organization)
            .join(Organization.activities)
            .filter(Activity.id.in_(activity_ids))
            .all()
        )

    def search_by_name(self, db: Session, name: str) -> list[Organization]:
        """
        Поиск организаций по названию
        (частичное совпадение, регистронезависимо).
        """
        return (
            db.query(Organization)
            .filter(Organization.name.ilike(f"%{name}%"))
            .all()
        )


crud_organization = CRUDOrganization(Organization)
