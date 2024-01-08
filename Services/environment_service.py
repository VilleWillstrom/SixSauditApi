from typing import Annotated

from fastapi import Depends

import models
from Services.base_service import BaseService
from dtos.environment import EnvironmentCreateReq


class EnvironmentService(BaseService):
    def __init__(self, db: models.Db):
        # Initialize EnvironmentService with a database instance
        super(EnvironmentService, self).__init__(db)

    def get_all_environments(self):
        # Get all environments from the database
        environments = self.db.query(models.Environment).all()
        return environments


    def get_environment_by_id(self, _id):
        # Get an environment by its ID from the database
        environment = self.db.query(models.Environment).get(_id)
        return environment

    def get_environments_by_location_id(self, location_id):
        # Get all environments based on the location ID
        environments = self.db.query(models.Environment).filter(models.Environment.location_id == location_id).all()
        return environments

    def add_environment(self, environment: EnvironmentCreateReq):
        self.db.add(models.Environment(
            name=environment.name,
            description=environment.description,
            location_id=environment.location_id,
            environmenttype_id=environment.environmenttype_id
        ))
        self.db.commit()

    def update_environment_by_id(self, new_environment: models.Environment):
        pass

    def delete_environment_by_id(self, _id: int):
        self.db.query(models.Environment).where(models.Environment.id == _id).delete()
        self.db.commit()


def init_environment_service(db: models.Db):
    return EnvironmentService(db)


EnvironmentServ = Annotated[EnvironmentService, Depends(init_environment_service)]
