from pydantic import BaseModel


class Environment(BaseModel):
    id: int
    name: str


class LocationCreateReq(BaseModel):
    name: str
    address: str
    zip_code: str


class EnvironmentTypeCreateReq(BaseModel):
    name: str


class EnvironmentCreateReq(BaseModel):
    name: str
    description: str
    location_id: int
    environmenttype_id: int
