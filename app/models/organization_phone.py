from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.base import Base


class OrganizationPhone(Base):
    __tablename__ = "organization_phones"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    phone_number = Column(
        String,
        nullable=False
    )
    organization_id = Column(
        Integer,
        ForeignKey("organizations.id", ondelete="CASCADE")
    )

    organization = relationship(
        "Organization",
        back_populates="phones"
    )
