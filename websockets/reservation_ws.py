from fastapi.websockets import WebSocket

connected_clients = []

async def reservation_ws(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            for client in connected_clients:
                await client.send_text(f"New reservation update: {data}")
    except:
        connected_clients.remove(websocket)
