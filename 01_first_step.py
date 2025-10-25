from fastapi import FastAPI             #imports the core application class from the FastAPI framework

app = FastAPI()                         #initialises the FastAPI class to create an application object(which serves as the central router and request handler for the API). The "app" variable is the "insance" of the class FastAPI.

@app.get("/")                           #This is a router decorator(used to map HTTP methods and paths to python functions) that registers a GET endpoint at the root path and run the function below.
async def root():                       #asynchronous route handler function. async allows FastAPI to handle concurrent requests.
    return {"message": "Hello World"}   #this resturns a dictionary as response, which FastAPI automatically serializes into a JSON response.