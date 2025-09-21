from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from app.core.base import Base

# Ассоциация организация ↔ деятельность
organization_activity = Table(
    "organization_activity",
    Base.metadata,
    Column(
        "organization_id",
        Integer,
        ForeignKey("organizations.id"),
        primary_key=True
    ),
    Column(
        "activity_id",
        Integer,
        ForeignKey("activities.id"),
        primary_key=True
    ),
)


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    name = Column(
        String,
        nullable=False,
        unique=True
    )
    building_id = Column(
        Integer,
        ForeignKey("buildings.id"),
        nullable=False
    )

    building = relationship(
        "Building",
        back_populates="organizations"
    )
    phones = relationship(
        "OrganizationPhone",
        back_populates="organization",
        cascade="all, delete-orphan"
    )
    activities = relationship(
        "Activity",
        secondary=organization_activity,
        back_populates="organizations"
    )
