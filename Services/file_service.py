from typing import Annotated

from fastapi import Depends

import models
from Services.base_service import BaseService


class FileService(BaseService):
    def __int__(self, db: models.Db):
        super(FileService, self).__init__(db)

    def upload(self, form_id: int, original_name: str, random_name: str):
        file = models.File(inspectionform_id=form_id, original_name=original_name, random_name=random_name)
        self.db.add(file)
        self.db.commit()
        return True


def init_file_service(db: models.Db):
    return FileService(db)


FileServ = Annotated[FileService, Depends(init_file_service)]
