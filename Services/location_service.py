from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy import exists

import models
from Services.base_service import BaseService
from dtos.location import LocationCreateReq


class LocationService(BaseService):
    def __init__(self, db: models.Db):
        # Initialize LocationService with a database instance
        super(LocationService, self).__init__(db)

    def get_all_locations(self):
        # Get all locations from the database
        return self.db.query(models.Location).all()

    def _check_name_existence(self, name: str):
        # Check if a location with the given name exists in the database
        return self.db.query(exists().where(models.Location.name == name)).scalar()

    def add_location(self, location: LocationCreateReq):
        # Add a new location to the database, checking for name existence
        if not self._check_name_existence(location.name):
            self.db.add(models.Location(name=location.name, address=location.address, zip_code=location.zip_code))
            self.db.commit()
        else:
            raise HTTPException(status_code=403, detail="Location with that name already exists")

    def get_location_by_id(self, _id):
        # Get location by ID from the database
        return self.db.query(models.Location).get(_id)

    def _check_location_existence(self, _id: int):
        # Check if a location with the given ID exists in the database
        return self.db.query(exists().where(models.Location.id == _id)).scalar()

    def _check_update_constraints(self, new_location: models.Location):
        # Check constraints before updating a location
        location_is_existing = self._check_location_existence(new_location.id)
        name_is_existing = self._check_name_existence(new_location.name)

        if not location_is_existing:
            raise HTTPException(status_code=404, detail="Location was not found")

        if name_is_existing:
            raise HTTPException(status_code=403, detail="Location with that name already exists")

    def update_location_by_id(self, new_location: models.Location):
        # Update location by ID in the database, checking constraints
        self._check_update_constraints(new_location)

        self.db.query(models.Location).filter(models.Location.id == new_location.id).update(
            {"id": new_location.id,
             "name": new_location.name,
             "address": new_location.address,
             "zip_code": new_location.zip_code}
        )
        self.db.commit()

    def delete_location_by_id(self, _id: int):
        # Delete location by ID from the database
        if self._check_location_existence(_id):
            self.db.query(models.Location).filter(models.Location.id == _id).delete()
            self.db.commit()
        else:
            raise HTTPException(status_code=404, detail="Location was not found")


def init_location_service(db: models.Db):
    # Initialize LocationService with a database instance
    return LocationService(db)


LocationServ = Annotated[LocationService, Depends(init_location_service)]
