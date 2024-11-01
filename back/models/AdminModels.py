from pydantic import BaseModel, EmailStr 
from typing import List , Optional
from fastapi.responses import FileResponse

class UserList(BaseModel):
    id : int
    name : str
    surname : str
    email : EmailStr