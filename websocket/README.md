# Real-Time Bidirectional Chat with FastAPI WebSockets

This file demonstrates a  pattern for handling persistent, full-duplex communication using **FastAPI** and the **WebSocket API**. Unlike standard RESTful APIs, this system maintains a stateful connection between the client and the server.

## 1. Technical Architecture & Lifecycle

The following diagram illustrates the transition from a stateless HTTP request to a stateful WebSocket stream, managed by the `ConnectionManager`.
![](https://github.com/uv-goswami/API/blob/13ec3222b04af1ec08ebf066f60fd572adf973a8/websocket/01_connection_lifecycle.png)

### The 4 Phases of a WebSocket Lifecycle

1. **HTTP Handshake (Phase 1):** The client requests the UI via a standard `GET` request. The server returns an `HTMLResponse`.
2. **Protocol Upgrade (Phase 2):** The browser initiates a specialized request with the header `Upgrade: websocket`. FastAPI's `@app.websocket` router intercepts this, switching the protocol from HTTP to WS (Code 101).
3. **The Event Loop (Phase 3):** An asynchronous `while True` loop keeps the execution context alive. The server "waits" (non-blocking) for incoming text frames and broadcasts them to all stored memory addresses in the `active_connections` list.
4. **Termination (Phase 4):** When a user closes their tab, the TCP connection breaks, triggering a `WebSocketDisconnect` exception. The server catches this to perform "Garbage Collection" by removing the socket from the active list.

---

## 2. Core Implementation

### The Connection Manager (The "Switchboard")

The `ConnectionManager` is a singleton-style class that manages the **State** of the application. Because WebSockets are stateful, the server must keep track of every connected client in the **Heap Memory**.

```python
class ConnectionManager:
    def __init__(self):
        # Stores memory references to active WebSocket objects
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        # Completes the Handshake
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        # Prevents Memory Leaks by removing stale connections
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        # O(n) operation: Iterates through all connections
        for connection in self.active_connections:
            await connection.send_text(message)

```

### The WebSocket Endpoint

The endpoint handles the **IO-Bound** tasks. Using `async/await` is critical here; it ensures that if one client has high latency, the Python **Event Loop** can still process messages for other users.

```python
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            # Server pauses here until a frame is received
            data = await websocket.receive_text()
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        # Triggered by client-side closure (e.g., closing browser tab)
        manager.disconnect(websocket)
        print(f"Client #{client_id} disconnected")

```

---

## 3. Technical Concepts Explained

### Why `async def` and `await`?

In a WebSocket context, the server is often idle, waiting for data to travel across the internet. `await` allows the CPU to "yield control," meaning it can handle thousands of concurrent connections on a single thread without blocking.

### Memory Management (The List)

The `active_connections` list resides in the server's RAM.

* **Connection:** We push the `WebSocket` object into the list.
* **Disconnection:** We must `remove` it. Failing to do so causes a **Memory Leak**, where the list grows indefinitely with "dead" connections, eventually crashing the server.

### The Frontend (JavaScript)

The client-side uses the native `window.WebSocket` object. Note the URL scheme change:

* `http://` becomes `ws://`
* `https://` becomes `wss://` (Secure)

```javascript
// Dynamic ID generation to identify the session
var client_id = Date.now();
var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);

ws.onmessage = function(event) {
    // Logic to inject received text into the DOM
};

```

---

## 4. How to Run

1. Install requirements: `pip install fastapi`
2. Run the server: `fastapi dev websocket_01.py` (Change the File Names accordingly)
3. Open `http://localhost:8000` in multiple browser tabs to test the real-time broadcast.

## 5. Demonstration
![](https://github.com/uv-goswami/API/blob/eac6ac7ef786fe9f8dbded7e894d8db51079a121/websocket/browser_inteface.png)
![](https://github.com/uv-goswami/API/blob/eac6ac7ef786fe9f8dbded7e894d8db51079a121/websocket/terminal_interface.png)
