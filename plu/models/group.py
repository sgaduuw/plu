from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from plu.database import Base


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)

    # Establish the relationship with users
    users = relationship("User", back_populates="group")
