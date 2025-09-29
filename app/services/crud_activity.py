from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.activity import Activity
from app.schemas.activity import ActivityCreate
from app.services.base import CRUDBase


class CRUDActivity(CRUDBase):
    """
    CRUD для деятельностей с проверкой
    уровня вложенности (асинхронный).
    """

    async def create(
            self,
            obj_in: ActivityCreate,
            db: AsyncSession
    ) -> Activity:
        """
        Создаёт активность с ограничением
        вложенности не более 3 уровней.
        """
        parent_id = obj_in.parent_id
        if parent_id:
            depth = await self._get_depth(db, parent_id)
            if depth >= 3:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        "Максимальный уровень вложенности деятельностей — 3."
                    )
                )

        db_obj = Activity(**obj_in.dict())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def _get_depth(self, db: AsyncSession, parent_id: int) -> int:
        """Возвращает глубину дерева для родителя."""
        depth = 1
        current = await db.get(Activity, parent_id)

        while current and current.parent_id:
            depth += 1
            current = await db.get(Activity, current.parent_id)

        return depth

    async def get_descendants(
            self,
            db: AsyncSession,
            activity_id: int
    ) -> list[Activity]:
        """Возвращает всех потомков активности (вложенные до 3 уровней)."""
        descendants = []
        stack = [activity_id]

        while stack:
            current_id = stack.pop()
            result = await db.execute(
                select(Activity).where(Activity.parent_id == current_id)
            )
            children = result.scalars().all()
            for child in children:
                descendants.append(child)
                stack.append(child.id)

        return descendants


activity_crud = CRUDActivity(Activity)
