from sqlalchemy import select
from sqlalchemy.orm import Session


class CRUDBase:

    def __init__(self, model):
        self.model = model

    def get(
        self,
        obj_id: int,
        session: Session,
    ):
        db_obj = session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    def get_multi(
        self,
        session: Session
    ):
        db_objs = session.execute(select(self.model))
        return db_objs.scalars().all()

    def create(
        self,
        obj_in,
        session: Session,
    ):
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def remove(
        self,
        db_obj,
        session: Session,
    ):
        session.delete(db_obj)
        session.commit()
        return db_obj
