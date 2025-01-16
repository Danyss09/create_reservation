from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.database import get_db_connection
from datetime import datetime, time

app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Welcome to the Reservation Service!"}

# Definir el modelo de datos que recibirá la solicitud
class ReservationCreate(BaseModel):
    customer_id: int
    restaurant_id: int
    date: datetime  # Usamos datetime en lugar de str
    time: str  # Usamos str y luego lo convertimos
    guests: int

    # Convertir la hora en el formato adecuado (hora: minutos)
    def get_time(self):
        return datetime.strptime(self.time, "%H:%M").time()

# Ruta para crear una nueva reserva
@app.post("/create")
async def create_reservation(reservation: ReservationCreate):
    connection = await get_db_connection()
    try:
        # Comprobar si la reserva ya existe para el mismo cliente, restaurante, fecha y hora
        check_query = """
        SELECT COUNT(*) FROM Reservations 
        WHERE CustomerID = $1 AND RestaurantID = $2 AND Date = $3 AND Time = $4;
        """
        exists = await connection.fetchval(check_query, reservation.customer_id, reservation.restaurant_id, reservation.date.date(), reservation.get_time())

        if exists > 0:
            raise HTTPException(status_code=400, detail="Reservation already exists for the given customer, restaurant, date, and time.")
        
        # Insertar la nueva reserva
        insert_query = """
        INSERT INTO Reservations (CustomerID, RestaurantID, Date, Time, Guests)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING ReservationID;
        """
        reservation_id = await connection.fetchval(insert_query, reservation.customer_id, reservation.restaurant_id, reservation.date.date(), reservation.get_time(), reservation.guests)
        
        # Responder con un mensaje de éxito
        return {"message": "Reservation created successfully", "reservation_id": reservation_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    finally:
        await connection.close()
