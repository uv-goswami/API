from fastapi import FastAPI, WebSocket, WebSocketDisconnect
#WebSocket: provides the methods to talk to the cleint and server. It is Bidirectional and remains open throughout the session.
#WebSocketDisconnect : It is an exception, that is triggered when the client leaves the conversation.

'''from typing import List '''


app = FastAPI()


#Defining a class(Bueprint) ConnectionManager(it is not a built-in Fastapi tool)
class ConnectionManager:
    
    #initializing a constructor that runs automatically the very moment the manager is created to prepare the environment.. 
    def __init__(self):     #self allows the function to talk to active_connection list
        #creates an empty list inside the manager to store te Websocket connections that stays open
        self.active_connections: list[WebSocket] = []


    #Asynchronous (used when a function needs to await something)function that handles a new person trying to connect
    async def connect(self, websocket: WebSocket):  #websocket is the variable name for the specific connection currently trying to join. We can name it anything like ws....
        #Add the active connections to the active_connections list.
        self.active_connections.append(websocket)

    #Function to clean the list by removing the users when they leave the connection to prevent Memory Leak
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connnections :
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connec(websocket)

    await websocket.send_text("Hello! Message From Server!!")

    try:
        wjile True:

        data = await websocket.receive_text()

        await manager.broadcast(data)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Client disconnected")


