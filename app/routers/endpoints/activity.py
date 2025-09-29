# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session

# from app.schemas.activity import ActivityCreate, ActivityRead
# from app.services.crud_activity import activity_crud
# from app.core.database import get_db
# from app.services.validators import (
#     check_activity_exists,
#     check_activity_level_limit,
#     check_activity_name_duplicate,
# )
# router = APIRouter()


# @router.post(
#     "/",
#     response_model=ActivityRead,
#     summary="Создать новый вид деятельности",
#     description="Добавляет новый вид деятельности в справочник. "
#                 "Можно указать родительский вид для построения дерева."
# )
# def create_activity(activity: ActivityCreate, db: Session = Depends(get_db)):
#     check_activity_name_duplicate(db, activity.name)
#     new_activity = activity_crud.create(activity, db)
#     check_activity_level_limit(new_activity)
#     return new_activity


# @router.get(
#     "/",
#     response_model=list[ActivityRead],
#     summary="Список всех видов деятельности",
#     description=(
#         "Возвращает древовидный список всех доступных видов деятельности."
#     )
# )
# def list_activities(db: Session = Depends(get_db)):
#     return activity_crud.get_multi(db)


# @router.get(
#     "/{activity_id}",
#     response_model=ActivityRead,
#     summary="Получить вид деятельности по ID",
#     description=(
#         "Возвращает информацию о виде деятельности, включая дочерние элемент
#     )
# )
# def get_activity(activity_id: int, db: Session = Depends(get_db)):
#     check_activity_exists(db, activity_id)
#     return activity_crud.get(activity_id, db)
# secunda_test_task/app/routers/endpoints/activity.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.activity import ActivityCreate, ActivityRead
from app.services.crud_activity import activity_crud
from app.core.database import get_db
from app.services.validators import (
    check_activity_exists,
    check_activity_level_limit,
    check_activity_name_duplicate,
)

router = APIRouter()


@router.post(
    "/",
    response_model=ActivityRead,
    summary="Создать новый вид деятельности",
    description=(
        "Добавляет новый вид деятельности в справочник. "
        "Можно указать родительский вид для построения дерева."
    )
)
async def create_activity(
    activity: ActivityCreate,
    db: AsyncSession = Depends(get_db)
):
    await check_activity_name_duplicate(db, activity.name)
    new_activity = await activity_crud.create(activity, db)
    check_activity_level_limit(new_activity)
    return new_activity


@router.get(
    "/",
    response_model=list[ActivityRead],
    summary="Список всех видов деятельности",
    description=(
        "Возвращает древовидный список всех доступных видов деятельности."
    )
)
async def list_activities(db: AsyncSession = Depends(get_db)):
    return await activity_crud.get_multi(db)


@router.get(
    "/{activity_id}",
    response_model=ActivityRead,
    summary="Получить вид деятельности по ID",
    description=(
        "Возвращает информацию о виде деятельности,"
        "включая дочерние элементы."
    )
)
async def get_activity(activity_id: int, db: AsyncSession = Depends(get_db)):
    await check_activity_exists(db, activity_id)
    return await activity_crud.get(activity_id, db)
