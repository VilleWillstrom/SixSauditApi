from pydantic import BaseModel
from typing import Optional


class InspectionFormQuestion(BaseModel):
    id: int
    question_type: str
    question_text: str
    choices: Optional[str]


class InspectionFormQuestionCreateReq(BaseModel):
    question_type: str
    question_text: str
    choices: Optional[str]