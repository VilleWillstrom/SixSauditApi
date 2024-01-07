from typing import Annotated

from fastapi import Depends

import models
from Services.base_service import BaseService


class FileService(BaseService):
    def __init__(self, db: models.Db):
        # Initialize FileService with a database instance
        super(FileService, self).__init__(db)

    def upload(self, form_id: int, original_name: str, random_name: str):
        # Upload a file to the database
        file = models.File(inspectionform_id=form_id, original_name=original_name, random_name=random_name)
        self.db.add(file)
        self.db.commit()
        return True


def init_file_service(db: models.Db):
    # Initialize FileService with a database instance
    return FileService(db)


FileServ = Annotated[FileService, Depends(init_file_service)]
