# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session

# from app.core.database import get_db
# from app.schemas.building import BuildingCreate, BuildingRead
# from app.services.crud_building import crud_building
# from app.services.validators import (
#     check_building_address_duplicate,
#     check_building_exists
# )

# router = APIRouter()


# @router.post(
#     "/",
#     response_model=BuildingRead,
#     summary="Создать новое здание",
#     description="Добавляет новое здание с адресом и координатами."
# )
# def create_building(building: BuildingCreate, db: Session = Depends(get_db)):
#     check_building_address_duplicate(db, building.address)
#     return crud_building.create(building, db)


# @router.get(
#     "/",
#     response_model=list[BuildingRead],
#     summary="Список всех зданий",
#     description="Возвращает список зданий с адресами и координатами."
# )
# def list_buildings(db: Session = Depends(get_db)):
#     return crud_building.get_multi(db)


# @router.get(
#     "/{building_id}",
#     response_model=BuildingRead,
#     summary="Получить здание по ID",
#     description="Возвращает информацию о здании по его идентификатору."
# )
# def get_building(building_id: int, db: Session = Depends(get_db)):
#     check_building_exists(db, building_id)
#     return crud_building.get(building_id, db)
# secunda_test_task/app/routers/endpoints/building.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.building import BuildingCreate, BuildingRead
from app.services.crud_building import crud_building
from app.services.validators import (
    check_building_address_duplicate,
    check_building_exists
)

router = APIRouter()


@router.post(
    "/",
    response_model=BuildingRead,
    summary="Создать новое здание",
    description="Добавляет новое здание с адресом и координатами."
)
async def create_building(
    building: BuildingCreate,
    db: AsyncSession = Depends(get_db)
):
    await check_building_address_duplicate(db, building.address)
    return await crud_building.create(building, db)


@router.get(
    "/",
    response_model=list[BuildingRead],
    summary="Список всех зданий",
    description="Возвращает список зданий с адресами и координатами."
)
async def list_buildings(db: AsyncSession = Depends(get_db)):
    return await crud_building.get_multi(db)


@router.get(
    "/{building_id}",
    response_model=BuildingRead,
    summary="Получить здание по ID",
    description="Возвращает информацию о здании по его идентификатору."
)
async def get_building(building_id: int, db: AsyncSession = Depends(get_db)):
    await check_building_exists(db, building_id)
    return await crud_building.get(building_id, db)
