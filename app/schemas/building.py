from pydantic import BaseModel, field_validator


class BuildingBase(BaseModel):
    """Схема для создания здания."""
    address: str
    latitude: float
    longitude: float

    @field_validator("latitude")
    def validate_latitude(cls, v):
        if not -90 <= v <= 90:
            raise ValueError("Широта должна быть в пределах [-90, 90]")
        return v

    @field_validator("longitude")
    def validate_longitude(cls, v):
        if not -180 <= v <= 180:
            raise ValueError("Долгота должна быть в пределах [-180, 180]")
        return v


class BuildingCreate(BuildingBase):
    pass


class BuildingRead(BuildingBase):
    id: int

    class Config:
        orm_mode = True
