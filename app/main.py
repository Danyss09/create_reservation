# app/main.py
from fastapi import FastAPI, HTTPException
from app.database import get_db_connection

app = FastAPI()

# Ruta para crear una nueva reserva
@app.post("/create")
async def create_reservation(customer_id: int, restaurant_id: int, date: str, time: str, guests: int):
    connection = await get_db_connection()
    try:
        # Comprobar si la reserva ya existe para el mismo cliente, restaurante, fecha y hora
        check_query = """
        SELECT COUNT(*) FROM Reservations 
        WHERE CustomerID = $1 AND RestaurantID = $2 AND Date = $3 AND Time = $4;
        """
        exists = await connection.fetchval(check_query, customer_id, restaurant_id, date, time)
        
        if exists > 0:
            raise HTTPException(status_code=400, detail="Reservation already exists for the given customer, restaurant, date, and time.")
        
        # Insertar la nueva reserva
        insert_query = """
        INSERT INTO Reservations (CustomerID, RestaurantID, Date, Time, Guests)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING ReservationID;
        """
        reservation_id = await connection.fetchval(insert_query, customer_id, restaurant_id, date, time, guests)
        
        # Responder con un mensaje de éxito
        return {"message": "Reservation created successfully", "reservation_id": reservation_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    finally:
        await connection.close()
