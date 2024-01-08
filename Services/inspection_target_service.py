from sqlalchemy import exists
from typing import Annotated

from fastapi import Depends, HTTPException

import models
from Services.base_service import BaseService
from dtos.target import InspectionTargetCreateReq


class InspectionTargetService(BaseService):
    def __init__(self, db: models.Db):
        super(InspectionTargetService, self).__init__(db)

    def get_all_inspection_targets(self):
        # Get all inspection targets from the database
        inspection_targets = self.db.query(models.Inspectiontarget).all()
        return inspection_targets

    def get_all_inspection_targets_by_environment_id(self, environment_id):
        # Get all inspection targets that are related to specific environment from the database
        inspetion_targets = self.db.query(models.Inspectiontarget).filter(models.Inspectiontarget.environment_id == environment_id).all()
        return inspetion_targets

    def get_inspection_target_by_id(self, _id):
        # Get inspection target by ID from the database
        inspection_target = self.db.query(models.Inspectiontarget).get(_id)
        return inspection_target

    def add_inspection_target(self, inspection_target: InspectionTargetCreateReq):
        # Check if environment_id and inspectiontargettype_id exist before adding the inspection target
        self._check_environment_and_type_exist(inspection_target.environment_id, inspection_target.inspectiontargettype_id)

        # Add a new inspection target to the database
        self.db.add(models.Inspectiontarget(
            name=inspection_target.name,
            description=inspection_target.description,
            createdAt=inspection_target.createdAt,
            environment_id=inspection_target.environment_id,
            inspectiontargettype_id=inspection_target.inspectiontargettype_id
        ))
        self.db.commit()

    def update_inspection_target_by_id(self, new_inspection_target: models.Inspectiontarget):
        # Check if environment_id and inspectiontargettype_id exist before updating the inspection target
        self._check_environment_and_type_exist(new_inspection_target.environment_id, new_inspection_target.inspectiontargettype_id)

        # Check if the inspection target exists before updating
        is_existing = self.db.query(exists().where(models.Inspectiontarget.id == new_inspection_target.id)).scalar()

        if is_existing:
            # Update the inspection target in the database
            self.db.query(models.Inspectiontarget).filter(
                models.Inspectiontarget.id == new_inspection_target.id).update(
                {
                    "id": new_inspection_target.id,
                    "name": new_inspection_target.name,
                    "description": new_inspection_target.description,
                    "createdAt": new_inspection_target.createdAt,
                    "environment_id": new_inspection_target.environment_id,
                    "inspectiontargettype_id": new_inspection_target.inspectiontargettype_id
                }
            )
            self.db.commit()
        else:
            raise HTTPException(status_code=404, detail="Inspection target was not found")

    def delete_inspection_target_by_id(self, _id: int):
        # Check if the inspection target exists before deleting
        existing_inspection_target = self.get_inspection_target_by_id(_id)
        if not existing_inspection_target:
            raise HTTPException(status_code=404, detail="Inspection target not found")

        # Delete the inspection target from the database
        self.db.query(models.Inspectiontarget).filter(models.Inspectiontarget.id == _id).delete()
        self.db.commit()

    def _check_environment_and_type_exist(self, environment_id: int, inspectiontargettype_id: int):
        # Check if environment_id and inspectiontargettype_id exist in the database
        environment_is_existing = self.db.query(exists().where(models.Environment.id == environment_id)).scalar()
        inspection_target_type_is_existing = self.db.query(exists().where(models.Inspectiontargettype.id == inspectiontargettype_id)).scalar()

        if not environment_is_existing or not inspection_target_type_is_existing:
            # If either environment or inspectiontargettype is not found, raise an HTTPException
            raise HTTPException(status_code=400, detail="Invalid request. Environment or Inspectiontargettype not found.")

        return True


def init_inspection_target_service(db: models.Db):
    return InspectionTargetService(db)


InspectionTargetServ = Annotated[InspectionTargetService, Depends(init_inspection_target_service)]
