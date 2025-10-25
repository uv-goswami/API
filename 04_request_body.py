from fastapi import FastAPI
from pydantic import BaseModel          #pydantic is data validation library, BaseModel is the base class to define structured request/ response schemas. It automaticallly validates types, parses data and provides .model_dump() for serialization

class Item(BaseModel):                  #defines Pydantic model named Item. It represents the expected structure of request body.
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()                 # Creates an instance of the FastAPI application

@app.post("/items")             #defines POST endpoint at /items.
async def create_item(item: Item):          #tells DastAPI to Parse the reqyest body as JSON, validate it against Item model and inject the parsed Item object into the function
    item_dict = item.model_dump()           #Converts the Item object into dictionary, used to modify or return data
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

@app.put("/items/{item_id}")                #defines PUT endpoint at path parameter item_id
async def update_item(item_id: int, item: Item, q: str | None = None):      # item is request bpdy validated as Item
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result