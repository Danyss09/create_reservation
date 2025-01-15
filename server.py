import asyncio
import websockets
import json
import mysql.connector

# Función para conectarse a la base de datos
def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            database="ReservationDb",
            user="root",  # Cambia esto si usas otro usuario
            password="dani0919"  # Cambia esto por la contraseña que has configurado
        )
        if conn.is_connected():
            return conn
    except mysql.connector.Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

# Función para manejar las reservas
async def handle_create_reservation(websocket, path):
    data = await websocket.recv()
    reservation_data = json.loads(data)

    # Extraer la información de la reserva del mensaje recibido
    customer_id = reservation_data['CustomerID']
    restaurant_id = reservation_data['RestaurantID']
    date = reservation_data['Date']
    time = reservation_data['Time']
    guests = reservation_data['Guests']

    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Reservations (CustomerID, RestaurantID, Date, Time, Guests) VALUES (%s, %s, %s, %s, %s)",
            (customer_id, restaurant_id, date, time, guests)
        )
        conn.commit()
        cursor.close()
        conn.close()

        response = {"message": "Reservation created successfully!"}
    else:
        response = {"message": "Failed to connect to database"}

    # Enviar una respuesta al cliente WebSocket
    await websocket.send(json.dumps(response))

# Iniciar el servidor WebSocket
async def start_server():
    server = await websockets.serve(handle_create_reservation, "localhost", 8765)
    await server.wait_closed()

# Ejecutar el servidor
if __name__ == "__main__":
    asyncio.run(start_server())
