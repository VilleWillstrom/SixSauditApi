from typing import Annotated

from fastapi import Depends

import models
from Services.base_service import BaseService


class InspectionFormService(BaseService):
    def __init__(self, db: models.Db):
        super(InspectionFormService, self).__init__(db)

    def get_by_id(self, _id: int):
        return self.db.query(models.Inspectionform).filter(models.Inspectionform.id == _id).first()


def init_form_service(db: models.Db):
    return InspectionFormService(db)


FormServ = Annotated[InspectionFormService, Depends(init_form_service)]
