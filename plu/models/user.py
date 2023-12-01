from passlib.context import CryptContext
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from plu.database import Base

# Create a CryptContext instance for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    group_id = Column(Integer, ForeignKey("groups.id"))

    group = relationship("Group", back_populates="users")
    transactions = relationship("Transactions", back_populates="initiator")

