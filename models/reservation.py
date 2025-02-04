from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from database.connection import Base

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, nullable=False)
    table_id = Column(Integer, nullable=False)
    reservation_time = Column(DateTime, nullable=False)
    status = Column(String(50), default="pending")  # pending, confirmed, cancelled
