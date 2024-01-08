import datetime
from typing import Optional, List

from pydantic import BaseModel

from dtos.environment import Environment
from dtos.file import File
from dtos.inspection_question import InspectionFormQuestion
from dtos.inspection_type import InspectionType
from dtos.target import Target
from dtos.user import User

"""
    id = Column(INTEGER(11), primary_key=True)
    createdAt = Column(DateTime, nullable=False)
    closedAt = Column(DateTime)
    user_id = Column(ForeignKey('user.id'), nullable=False, index=True)
    environment_id = Column(ForeignKey('environment.id'), index=True)
    inspectiontarget_id = Column(ForeignKey('inspectiontarget.id'), index=True)
    inspectiontype_id = Column(ForeignKey('inspectiontype.id'), nullable=False, index=True)

    environment = relationship('Environment')
    inspectiontarget = relationship('Inspectiontarget')
    inspectiontype = relationship('Inspectiontype')
    user = relationship('User')

    files = relationship('File')
"""


class Form(BaseModel):
    id: int
    createdAt: datetime.datetime
    closedAt: Optional[datetime.datetime] = None
    user: User
    environment: Optional[Environment] = None
    inspectiontarget: Optional[Target] = None
    inspectiontype: InspectionType
    files: List[File]
    questions: List[InspectionFormQuestion]


class InspectionFormCreateReq(BaseModel):
    createdAt: datetime.datetime
    closedAt: Optional[datetime.datetime] = None
    user_id: int
    environment_id: int
    inspectiontarget_id: int
    inspetiontype_id: int


class FormRes(BaseModel):
    form: Form
