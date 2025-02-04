from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from controllers.reservation_controller import create_reservation
from services.validation_service import validate_customer, validate_table
from database.connection import get_db

router = APIRouter()

@router.post("/create")
def create_reservation_endpoint(customer_id: int, table_id: int, reservation_time: str, db: Session = Depends(get_db)):
    if not validate_customer(customer_id):
        raise HTTPException(status_code=400, detail="Customer ID not found")
    
    if not validate_table(table_id):
        raise HTTPException(status_code=400, detail="Table ID not found")

    return create_reservation(db, customer_id, table_id, reservation_time)
