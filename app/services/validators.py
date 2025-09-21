from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Organization, Building, Activity


def check_organization_exists(
        db: Session, organization_id: int
) -> Organization:
    org = db.query(
        Organization
    ).filter(Organization.id == organization_id).first()
    if org is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Организация не найдена"
        )
    return org


def check_organization_name_duplicate(db: Session, name: str) -> None:
    if db.query(Organization).filter(Organization.name == name).first():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Организация с таким названием уже существует"
        )


def check_building_exists(db: Session, building_id: int) -> Building:
    building = db.query(Building).filter(Building.id == building_id).first()
    if building is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Здание не найдено"
        )
    return building


def check_building_address_duplicate(db: Session, address: str) -> None:
    if db.query(Building).filter(Building.address == address).first():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Здание с таким адресом уже существует"
        )


def check_activity_exists(db: Session, activity_id: int) -> Activity:
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if activity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вид деятельности не найден"
        )
    return activity


def check_activity_name_duplicate(db: Session, name: str) -> None:
    if db.query(Activity).filter(Activity.name == name).first():
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
