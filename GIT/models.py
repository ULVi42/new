from sqlmodel import SQLModel,Field
from typing import Optional
class User(SQLModel,table=True):
    name : str = Field(default=None)
    hashed_password : str = Field(default=None)
    role : str = Field(default="User")
