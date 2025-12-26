from fastapi import FastAPI         # Imports FastAPI - the framework , its like installing the kitchen control panel
from pydantic import BaseModel      # Import BaseModel from Pydantic, which lets you defince adn validata structured data. It is like setting rules for what a kitchen looks like , eg., every item must have a name adn price.

app = FastAPI()                     #Creates an Instance of your FastAPI app. This is like turning on the kitchen system. Now it can accepts commands(routes).

class Item(BaseModel):              #Defines the structure of an item using Pydantic. This is request and response model. This is like item blueprint. Every item must have a name and price.
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []

@app.post("/items/")                #defines a POST endpoint at /items/. 
async def create_item(item: Item) -> Item:          # It accepts an Item in the request body and returns the same Item. This is like saying: "Add a new item to the kitchen." We give it a tomato.
    return item                                 # and it confirms. "Got it, heres your tomato."



@app.get("/items/")                             # Defines GET endpoint at /items/. Returns a list of item objects. Its like saying "Show me what's in the kitchen". It returns a list of items already there.
async def read_items() -> list[Item]:           #defines a GET endpoint at /items/. It returns an existing Item
    return [
        Item(name="Portal Gun", price = 42.0),
        Item(name="Plumbus", price=32.0),
    ]

