from pydantic import BaseModel


class Location(BaseModel):
    id: int
    name: str
    address: str
    zip_code: str


class LocationCreateReq(BaseModel):
    name: str
    address: str
    zip_code: str
