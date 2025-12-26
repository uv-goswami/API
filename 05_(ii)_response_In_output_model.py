from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserIn(BaseModel):                    #This is a request model that defines the structure of incoming user data.
    username: str
    password: str
    email: EmailStr
    full_name: str| None = None

class UserOut(BaseModel):                   # This is the response model that defines what data gets sent back.
    username: str
    email: EmailStr
    full_name: str | None = None

@app.post("/user/", response_model=UserOut) #response_model is a special keyword that fastAPI uses to filter and validate responses. We can not use different at response_model.
async def create_user(user: UserIn) -> Any:
    return user                     #This returns UserIn but FastAPi filters and Validate it against UserOut as there's response_model that tells fastapi that the end response would be UserOut.

