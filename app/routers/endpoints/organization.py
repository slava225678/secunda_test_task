# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session

# from app.schemas.organization import OrganizationCreate, OrganizationRead
# from app.services.crud_organization import crud_organization
# from app.services.crud_building import crud_building
# from app.core.database import get_db
# from app.services.validators import (
#     check_activity_exists,
#     check_building_exists,
#     check_organization_exists,
#     check_organization_name_duplicate,
# )

# router = APIRouter()


# @router.post(
#     "/",
#     response_model=OrganizationRead,
#     summary="Создать организацию",
#     description="Создаёт новую организацию, с привязкой к зданию, телефонами
#                 "и одним или несколькими видами деятельности."
# )
# def create_organization(
#     org: OrganizationCreate,
#     db: Session = Depends(get_db)
# ):
#     check_organization_name_duplicate(db, org.name)
#     check_building_exists(db, org.building_id)
#     for activity_id in org.activity_ids or []:
#         check_activity_exists(db, activity_id)
#     return crud_organization.create_organization(db, org)


# @router.get(
#     "/",
#     response_model=list[OrganizationRead],
#     summary="Список всех организаций",
#     description="Возвращает полный список организаций с телефонами, "
#                 "зданиями и видами деятельности."
# )
# def list_organizations(
#     db: Session = Depends(get_db)
# ):
#     return crud_organization.get_multi(db)


# @router.get(
#     "/{organization_id}",
#     response_model=OrganizationRead,
#     summary="Получить организацию по ID",
#     description="Возвращает карточку организации по её идентификатору."
# )
# def get_organization(
#     organization_id: int,
#     db: Session = Depends(get_db)
# ):
#     check_organization_exists(db, organization_id)
#     return crud_organization.get(organization_id, db)


# @router.get(
#     "/by-building/{building_id}",
#     response_model=list[OrganizationRead],
#     summary="Организации в здании",
#     description=(
#         "Возвращает список организаций, находящихся в указанном здании."
#     )
# )
# def list_organizations_by_building(
#     building_id: int,
#     db: Session = Depends(get_db)
# ):
#     return crud_organization.get_by_building(db, building_id)


# @router.get(
#     "/by-activity/{activity_id}",
#     response_model=list[OrganizationRead],
#     summary="Организации по виду деятельности",
#     description="Возвращает список организаций,"
#                 "связанных с указанным видом деятельности."
# )
# def list_organizations_by_activity(
#     activity_id: int,
#     db: Session = Depends(get_db)
# ):
#     return crud_organization.get_by_activity(db, activity_id)


# @router.get(
#     "/search/",
#     response_model=list[OrganizationRead],
#     summary="Поиск организаций по названию",
#     description="Ищет организации по названию (частичное совпадение)."
# )
# def search_organizations(name: str, db: Session = Depends(get_db)):
#     return crud_organization.search_by_name(db, name)


# @router.get(
#     "/by-area/",
#     response_model=list[OrganizationRead],
#     summary="Организации в области на карте",
#     description="Возвращает список организаций, находящихся в зданиях, "
#                 "расположенных внутри заданного прямоугольника по координатам
# )
# def list_orgs_by_area(
#     min_lat: float,
#     max_lat: float,
#     min_lon: float,
#     max_lon: float,
#     db: Session = Depends(get_db)
# ):
#     buildings = crud_building.get_by_bounding_box(
#         db, min_lat, max_lat, min_lon, max_lon
#     )
#     building_ids = [b.id for b in buildings]
#     return crud_organization.get_by_buildings(db, building_ids)
# secunda_test_task/app/routers/endpoints/organization.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.organization import OrganizationCreate, OrganizationRead
from app.services.crud_organization import crud_organization
from app.services.crud_building import crud_building
from app.core.database import get_db
from app.services.validators import (
    check_activity_exists,
    check_building_exists,
    check_organization_exists,
    check_organization_name_duplicate,
)

router = APIRouter()


@router.post(
    "/",
    response_model=OrganizationRead,
    summary="Создать организацию",
    description=(
        "Создаёт новую организацию, с привязкой к зданию, телефонами "
        "и одним или несколькими видами деятельности."
    )
)
async def create_organization(
    org: OrganizationCreate,
    db: AsyncSession = Depends(get_db)
):
    await check_organization_name_duplicate(db, org.name)
    await check_building_exists(db, org.building_id)
    for activity_id in org.activity_ids or []:
        await check_activity_exists(db, activity_id)
    return await crud_organization.create_organization(db, org)


@router.get(
    "/",
    response_model=list[OrganizationRead],
    summary="Список всех организаций",
    description=(
        "Возвращает полный список организаций с телефонами, "
        "зданиями и видами деятельности."
    )
)
async def list_organizations(
    db: AsyncSession = Depends(get_db)
):
    return await crud_organization.get_multi(db)


@router.get(
    "/{organization_id}",
    response_model=OrganizationRead,
    summary="Получить организацию по ID",
    description="Возвращает карточку организации по её идентификатору."
)
async def get_organization(
    organization_id: int,
    db: AsyncSession = Depends(get_db)
):
    await check_organization_exists(db, organization_id)
    return await crud_organization.get(organization_id, db)


@router.get(
    "/by-building/{building_id}",
    response_model=list[OrganizationRead],
    summary="Организации в здании",
    description=(
        "Возвращает список организаций, находящихся в указанном здании."
        )
)
async def list_organizations_by_building(
    building_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await crud_organization.get_by_building(db, building_id)


@router.get(
    "/by-activity/{activity_id}",
    response_model=list[OrganizationRead],
    summary="Организации по виду деятельности",
    description=(
        "Возвращает список организаций,"
        "связанных с указанным видом деятельности."
    )
)
async def list_organizations_by_activity(
    activity_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await crud_organization.get_by_activity(db, activity_id)


@router.get(
    "/search/",
    response_model=list[OrganizationRead],
    summary="Поиск организаций по названию",
    description="Ищет организации по названию (частичное совпадение)."
)
async def search_organizations(name: str, db: AsyncSession = Depends(get_db)):
    return await crud_organization.search_by_name(db, name)


@router.get(
    "/by-area/",
    response_model=list[OrganizationRead],
    summary="Организации в области на карте",
    description=(
        "Возвращает список организаций, находящихся в зданиях, "
        "расположенных внутри заданного прямоугольника по координатам."
    )
)
async def list_orgs_by_area(
    min_lat: float,
    max_lat: float,
    min_lon: float,
    max_lon: float,
    db: AsyncSession = Depends(get_db)
):
    buildings = await crud_building.get_by_bounding_box(
        db, min_lat, max_lat, min_lon, max_lon
    )
    building_ids = [b.id for b in buildings]
    return await crud_organization.get_by_buildings(db, building_ids)
