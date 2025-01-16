from fastapi import FastAPI, WebSocket
from app.database import get_db_connection
from app.websocket import WebSocketManager

app = FastAPI()
websocket_manager = WebSocketManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            # Procesar el mensaje y enviar respuesta
            await websocket_manager.send_message({"message": "Data received", "data": data})
    except:
        await websocket_manager.disconnect(websocket)

@app.get("/reservations")
async def get_reservations():
    connection = await get_db_connection()
    reservations = await connection.fetch("SELECT * FROM Reservations;")
    await connection.close()
    return reservations
