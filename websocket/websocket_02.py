from fastapi import FastAPI, WebSocket, WebSocketDisconnect
#WebSocket: provides the methods to talk to the cleint and server. It is Bidirectional and remains open throughout the session.
#WebSocketDisconnect : It is an exception, that is triggered when the client leaves the conversation.

from fastapi.responses import HTMLResponse

'''from typing import List ''' #not compulsory


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

app = FastAPI()


#Defining a class(Bueprint) ConnectionManager(it is not a built-in Fastapi tool)
class ConnectionManager:
    
    #initializing a constructor that runs automatically the very moment the manager is created to prepare the environment.. 
    def __init__(self):     #self allows the function to talk to active_connection list
        #creates an empty list inside the manager to store te Websocket connections that stays open
        self.active_connections: list[WebSocket] = []


    #Asynchronous (used when a function needs to await something)function that handles a new person trying to connect
    async def connect(self, websocket: WebSocket):  #websocket is the variable name for the specific connection currently trying to join. We can name it anything like ws....
        await websocket.accept()
        #Add the active connections to the active_connections list.
        self.active_connections.append(websocket)

    #Function to clean the list by removing the users when they leave the connection to prevent Memory Leak
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    #async def: defines a coroutine, Using async ensures that if one client has a slow network(high latnecy), it doesnt block the server from attempting to send the message to the next client in  the list.
    #self: (Instance Reference) provides access to the class's state, especialy the active_connections list whoich resides in the server's RAM(Heap Memory).
    async def broadcast(self, message: str):

        for connection in self.active_connections :
        #for connection in..:(iterator) this is a O(n) operation where n is the number of active connections. the server must iterate through the memory addresses of every stored WebSocket obeject.
            await connection.send_text(message)
            #await: (Yielding Control): This is a checkpoint for the Python event Loop which when hit initiates the network "send and pauses the broadcast function allowing the CPU to handle other incoming requests"


manager = ConnectionManager()
#It creates an instance of the ConnectionManager class and allocates a block of memory(in Heap Memory) to store it.
#Instation: The process of creating a concrete object from a class blueprint

@app.get("/")
#It defines an HTTP GET endpoint at the root URL(/)
#Decorator: is a line starting with '@'. It tells the fastapi that this is a part RESTful Routing system and run the function when a GET request hits "/"
async def get():
    return HTMLResponse(html)
    #HTMLResponse sets the HTTP header Content-Type: text/html. Without this the browser may just show the code as plain text.



@app.websocket("/ws/{client_id}")
#It defines a WebSocket Route that accepts a dynamic variable(client_id)
#Protocol Switching(Handshake): Web Browsers start with an HTTP request that has a header:- Upgrade:websocket.
#@app.websocket decorator listens specifically for this Upgrade requests.

async def websocket_endpoint(websocket: WebSocket, client_id: int):

    await manager.connect(websocket)
    #it calls the connect method of the manager instance , that we created earler
    #await ensures the server can handle other tasks while the signal travels across the wire.

    #Event Loop
    try:  #Exception Handling
    #This prepares the server for the moment the connecion inevitably breaks.

        while True:
        #The Infinite Loop , it is the kifetime of the connection. As long as the loop runs the user is online.
            data = await websocket.receive_text()
            #the coode stops and waits for the client to actually send data.
            await manager.broadcast(f"Client #{client_id} says: {data}")
            #It takes the unique ID from the URL and the message from the user and merges them into a single Piece of text for the broadcast.

    except WebSocketDisconnect:
        #exception Handler that cathces a specific signal "WebSocketDisconnect"
        manager.disconnect(websocket)
        #Garbage Collector
        
        print("Client disconnected")


