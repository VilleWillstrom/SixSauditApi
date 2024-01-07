from pydantic import BaseModel


class Target(BaseModel):
    id: int
    name: str


class InspectionTargetCreateReq(BaseModel):
    id: int
    name: str
    description: str
    environment_id: int
    inspectiontargettype_id: int
