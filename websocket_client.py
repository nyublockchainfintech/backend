import asyncio
import websockets

async def send_message():
    async with websockets.connect("ws://localhost:8765") as websocket:
        await websocket.send("Hello, WebSocket server!")
        response = await websocket.recv()
        print(f"Response from server: {response}")

asyncio.get_event_loop().run_until_complete(send_message())

