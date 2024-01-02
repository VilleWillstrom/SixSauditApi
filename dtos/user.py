from pydantic import BaseModel


class User(BaseModel):
    id: int
    email: str


class AddNewUserReq(BaseModel):
    username: str
    password: str
    firstName: str
    lastName: str
    role: str


class AddNewUserRes(BaseModel):
    email: str
    id: int
    firstName: str
    lastName: str
    role: str
