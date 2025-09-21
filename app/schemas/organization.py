import re
from pydantic import BaseModel, field_validator
from typing import List, Optional
from app.schemas.building import BuildingRead
from app.schemas.activity import ActivityRead


class OrganizationPhone(BaseModel):
    phone_number: str

    class Config:
        orm_mode = True

    @field_validator("phone_number")
    def validate_phone(cls, v: str) -> str:
        # простой пример: допускаем цифры, +, -, скобки и пробелы
        if not re.match(r"^[\d\+\-\(\)\s]{5,20}$", v):
            raise ValueError("Неверный формат номера телефона")
        return v


class OrganizationBase(BaseModel):
    name: str
    building_id: int
    activity_ids: Optional[List[int]] = []

    @field_validator("name")
    def validate_name(cls, v: str) -> str:
        if len(v.strip()) < 2:
            raise ValueError(
                "Название организации должно содержать минимум 2 символа"
            )
        return v


class OrganizationCreate(OrganizationBase):
    phones: Optional[List[str]] = []

    @field_validator("phones")
    def validate_phones(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        if v:
            pattern = re.compile(r"^[\d\+\-\(\)\s]{5,20}$")
            for phone in v:
                if not pattern.match(phone):
                    raise ValueError(
                        f"Неверный формат номера телефона: {phone}"
                    )
        return v


class OrganizationRead(OrganizationBase):
    id: int
    building: "BuildingRead"  # forward reference
    phones: List[OrganizationPhone] = []
    activities: List["ActivityRead"] = []

    class Config:
        orm_mode = True
