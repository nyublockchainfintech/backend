import asyncio
import websockets
from fastapi import FastAPI, WebSocket

app = FastAPI()

# WebSocket handler
async def websocket_handler(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            message = await websocket.receive_text()
            await websocket.send_text(f"Received: {message}")
        except websockets.exceptions.ConnectionClosed:
            break

# HTTP endpoint to return instructions on how to connect to the WebSocket
@app.get('/')
async def index():
    return {"message": "WebSocket server running on ws://localhost:8765"}

# Start WebSocket server
async def start_websocket_server():
    server = await websockets.serve(websocket_handler, "localhost", 8765)
    await server.wait_closed()

# Run FastAPI app and WebSocket server
if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(start_websocket_server())
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

