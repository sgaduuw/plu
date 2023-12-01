from passlib.context import CryptContext
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship


from plu.database import Base

# Create a CryptContext instance for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Transactions(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Integer)
    price = Column(Integer)

    initiator = relationship("User", back_populates="transactions")

    def get_price_eur(self):
        return self.price / 100

    def set_price_eur(self, price_eur):
        self.price = price_eur * 100
