'''
⚠️ Note: This file contains multiple route definitions with the same path (/items/{item_id}), which will cause FastAPI to overwrite earlier routes. Only the last matching route will be active when the app runs.

This is intentional for learning purposes—we’re exploring different query parameter patterns and behaviors in isolation. In production, each route should have a unique path to avoid conflicts.
'''


from fastapi import FastAPI

app = FastAPI()

#A mock list of items used for testing.
fake_items_db = [{"item_name" : "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

#Pagination with Query Parameters
@app.get("/items/")
async def read_item(skip : int = 0, limit: int = 10):       #query parameters "skip" and "limit" are used to paginate(slice the dataset into chunks)
    return fake_items_db[skip: skip + limit]

#operational Parameters
@app.get("/items/{item_id}")
async def read_item(item_id: str, q:str | None = None):     #defines FastApi handler with one path parameter(item_id) and one optional query parameter(q). q can be a string OR none type but by default its none.
    if q:
        return {"item_id": item_id, "q": q}
    return{"item_id": item_id}

#Query parameter type conversion
@app.get("/items/{item_id}")
async def read_item(item_id: str, q:str | None = None, short: bool = False):    #short is a parameter whose type is Boolean and its default value if False
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item"}
        )
    return item


#Multiple path and Query Parameters
@app.get("/users/{user_id}/items/{item_id}")        #this route matches URL's like: "http://127.0.0.1:8000/users/7/items/pen"
async def read_user_item(
    user_id: int, item_id: str, q:str | None = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}        #dictionary with the item's ID and users ID
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item"}
        )
    return item

#Required query parameters
@app.get("/items/{item_id}")    
async def read_user_item(item_id: str, needy: str, skip: int = 0, limit: int | None=None):  #needy must be passed in query string like "?needy=value"
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item

