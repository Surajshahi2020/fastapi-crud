from pydantic import BaseModel

class UserCreate(BaseModel):
    id: int
    name: str
    email: str
    password: str

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True
