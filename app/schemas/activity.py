from pydantic import BaseModel, field_validator
from typing import List, Optional


class ActivityBase(BaseModel):
    name: str
    parent_id: Optional[int] = None

    @field_validator("name")
    def validate_name(cls, v: str) -> str:
        if len(v.strip()) < 2:
            raise ValueError(
                "Название деятельности должно содержать минимум 2 символа"
            )
        return v.strip()

    @field_validator("parent_id")
    def validate_parent_id(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v < 1:
            raise ValueError(
                "parent_id должен быть положительным числом или None"
            )
        return v


class ActivityCreate(ActivityBase):
    pass


class ActivityRead(ActivityBase):
    id: int
    children: List["ActivityRead"] = []

    class Config:
        orm_mode = True


# для рекурсивной схемы
ActivityRead.model_rebuild()
