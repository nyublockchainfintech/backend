import asyncio
import websockets

async def hello():
    async with websockets.connect("ws://localhost:8000/ws") as websocket:
        print("WebSocket is connected.")
        await websocket.send("Hello, server!")
        response = await websocket.recv()
        print("Message from server:", response)

asyncio.get_event_loop().run_until_complete(hello())

