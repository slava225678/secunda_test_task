from fastapi import APIRouter, Depends

from .endpoints import activity_router, building_router, organization_router
from app.core.dependencies import get_api_key


main_router = APIRouter()


main_router.include_router(
    building_router,
    prefix="/buildings",
    tags=["Buildings"],
    dependencies=[Depends(get_api_key)]
)
main_router.include_router(
    activity_router,
    prefix="/activities",
    tags=["Activities"],
    dependencies=[Depends(get_api_key)]
)
main_router.include_router(
    organization_router,
    prefix="/organizations",
    tags=["Organizations"],
    dependencies=[Depends(get_api_key)]
)
