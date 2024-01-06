from pydantic import BaseModel


class InspectionType(BaseModel):
    id: int
    name: str


class InspectionTypeCreateReq(BaseModel):
    name: str
