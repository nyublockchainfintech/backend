from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from ecdsa import SigningKey, VerifyingKey, NIST384p
import json
import base64
import logging
from fastapi.middleware.cors import CORSMiddleware

#ecdsa key generation

# Generating sample ECDSA keys for two users
client_private_keys = {
    1: SigningKey.generate(curve=NIST384p),
    2: SigningKey.generate(curve=NIST384p)
}

client_public_keys = {
    1: client_private_keys[1].verifying_key,
    2: client_private_keys[2].verifying_key
}

# Converting public keys to PEM format
client_public_keys_pem = {
    client_id: key.to_pem().decode() for client_id, key in client_public_keys.items()
}

#html for client's browser
html_template = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id">{client_id}</span></h2>
        <h3>Your Public Key:</h3>
        <pre id="public-key">{public_key}</pre>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = {client_id}; // Highlight: No change needed here as format() handles insertion.
            var public_key = `{public_key}`;
            document.querySelector("#ws-id").textContent = client_id.toString();
            document.querySelector("#public-key").textContent = public_key;
            // Highlight: Explicitly convert client_id to a string for WebSocket URL
            var ws = new WebSocket('ws://backend-production-d3db.up.railway.app/ws/' + client_id.toString());
            ws.onmessage = function(event) {{
                var messages = document.getElementById('messages');
                var message = document.createElement('li');
                var content = document.createTextNode(event.data);
                message.appendChild(content);
                messages.appendChild(message);
            }};
            function sendMessage(event) {{
                var input = document.getElementById("messageText");
                ws.send(input.value);
                input.value = '';
                event.preventDefault();
            }}
        </script>
    </body>
</html>
"""
# Initialize logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Stores active connections, allows messages from each individual client
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, client_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        logger.info(f"Client {client_id} connected")

    def disconnect(self, client_id: int):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            logger.info(f"Client {client_id} disconnected")

    async def send_personal_message(self, message: str, client_id: int):
        websocket = self.active_connections.get(client_id)
        if websocket:
            await websocket.send_text(message)
            logger.info(f"Sent personal message to client {client_id}: {message}")

    async def broadcast(self, message: str):
        for client_id, websocket in self.active_connections.items():
            try:
                await websocket.send_text(message)
                logger.info(f"Broadcast message to client {client_id}: {message}")
            except Exception as e:
                logger.error(f"Failed to send message to client {client_id}: {e}")

manager = ConnectionManager()

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "https://backend-production-d3db.up.railway.app/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/{client_id}")
async def get(client_id: int):
    if client_id not in client_public_keys_pem:
        raise HTTPException(status_code=404, detail="Client ID not found")
    public_key = client_public_keys_pem[client_id].replace("\n", "\\n")
    return HTMLResponse(html_template.format(client_id=client_id, public_key=public_key))

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    # Check origin header to ensure it's allowed
    origin = websocket.headers.get("origin")
    if origin not in origins:
        await websocket.close(code=1008)
        return
    
    await manager.connect(client_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        await manager.broadcast(f"Client #{client_id} left the chat")