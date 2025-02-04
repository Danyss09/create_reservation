from fastapi import FastAPI, WebSocket
from routes.reservation_routes import router as reservation_router
from websockets import reservation_ws
from database.connection import engine, Base

app = FastAPI()

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

# Incluir rutas
app.include_router(reservation_router, prefix="/reservations", tags=["Reservations"])

# WebSockets
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await reservation_ws(websocket)
