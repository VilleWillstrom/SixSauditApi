from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy import exists

import models
from Services.base_service import BaseService
from dtos.inspection_type import InspectionTypeCreateReq


class InspectionTypeService(BaseService):
    def __init__(self, db: models.Db):
        super(InspectionTypeService, self).__init__(db)

    def get_all_inspection_types(self):
        # Retrieve all inspection types
        return self.db.query(models.Inspectiontype).all()

    def _check_name_existence(self, name: str):
        # Check if an inspection type with the given name already exists
        return self.db.query(exists().where(models.Inspectiontype.name == name)).scalar()

    def add_inspection_type(self, inspection_type: InspectionTypeCreateReq):
        # Add a new inspection type if it does not already exist
        if not self._check_name_existence(inspection_type.name):
            self.db.add(models.Inspectiontype(name=inspection_type.name))
            self.db.commit()
        else:
            raise HTTPException(status_code=403, detail="Inspection type with that name already exists")

    def get_inspection_type_by_id(self, _id):
        # Retrieve an inspection type by its ID
        return self.db.query(models.Inspectiontype).get(_id)

    def _check_inspection_type_existence(self, _id: int):
        # Check if an inspection type with the given ID exists
        return self.db.query(exists().where(models.Inspectiontype.id == _id)).scalar()

    def _check_update_constraints(self, new_inspection_type: models.Inspectiontype):
        # Check constraints before updating an inspection type
        inspection_type_is_existing = self._check_inspection_type_existence(new_inspection_type.id)
        name_is_existing = self._check_name_existence(new_inspection_type.name)

        if not inspection_type_is_existing:
            raise HTTPException(status_code=404, detail="Inspection type was not found")

        if name_is_existing:
            raise HTTPException(status_code=403, detail="Inspection type with that name already exists")

    def update_inspection_type_by_id(self, new_inspection_type: models.Inspectiontype):
        # Update an inspection type by its ID
        self._check_update_constraints(new_inspection_type)

        self.db.query(models.Inspectiontype).filter(models.Inspectiontype.id == new_inspection_type.id).update(
            {"id": new_inspection_type.id, "name": new_inspection_type.name}
        )
        self.db.commit()

    def delete_inspection_type_by_id(self, _id: int):
        # Delete an inspection type by its ID if it exists
        if self._check_inspection_type_existence(_id):
            self.db.query(models.Inspectiontype).filter(models.Inspectiontype.id == _id).delete()
            self.db.commit()
        else:
            raise HTTPException(status_code=404, detail="Inspection type was not found")


def init_inspection_type_service(db: models.Db):
    # Initialize the InspectionTypeService
    return InspectionTypeService(db)


InspectionTypeServ = Annotated[InspectionTypeService, Depends(init_inspection_type_service)]
