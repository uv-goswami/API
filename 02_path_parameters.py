from enum import Enum               #imports built-in Enum clas, which lets us define a fixed set of named constants.

from fastapi import FastAPI

class ModelName(str, Enum):         #creates a custom ENUM called ModelName that inherits both str and Enum .
    alexnet = "alexnet"             #these are the allowed values
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()

@app.get("/models/{model_name}")    #this route listens to get request at the specified path. {model_name} is dynamic path parameter to validate against the Enum.
async def get_model(model_name: ModelName):    # this is the route handler 
    if model_name is ModelName.alexnet:         #checks if the Enum member is alexnet
        return {"model_name": model_name, "message ":  "Deep Learning FTW!"}
    
    if model_name.value == "lenet":
        return {"model_name" : model_name, "message": "LeCNN all the images"}
    
    return {"model_name": model_name, "message": "Have some residuals"}