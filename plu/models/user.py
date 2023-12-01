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
    hashed_password = Column(String)
    group_id = Column(Integer, ForeignKey("groups.id"))

    group = relationship("Group", back_populates="users")
    transactions = relationship("Transactions", back_populates="initiator")

    @classmethod
    def set_password(self, password):
        print(f"{password}")
        self.hashed_password = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.hashed_password)
