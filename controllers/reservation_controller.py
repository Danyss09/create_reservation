from sqlalchemy.orm import Session
from models.reservation import Reservation
from datetime import datetime

def create_reservation(db: Session, customer_id: int, table_id: int, reservation_time: str):
    new_reservation = Reservation(
        customer_id=customer_id,
        table_id=table_id,
        reservation_time=datetime.fromisoformat(reservation_time),
        status="pending"
    )
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    return new_reservation
