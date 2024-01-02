from fastapi import APIRouter

import models
from dtos.environment import EnvironmentTypeCreateReq, EnvironmentCreateReq, LocationCreateReq

router = APIRouter()


@router.post('/api/v1/location')
async def create(req: LocationCreateReq, db: models.Db):
    location = models.Location(
        name=req.name,
        address=req.address,
        zip_code=req.zip_code
    )

    db.add(location)
    db.commit()


@router.post('/api/v1/environment_type')
async def create(req: EnvironmentTypeCreateReq, db: models.Db):
    environment_type = models.Environmenttype(
        name=req.name
    )
    # Thanks to SQL Alchemy there's no need to write SQL queries.
    db.add(environment_type)  # makes an insert
    db.commit()  # commits an insert


@router.post('/api/v1/environment')
async def create(req: EnvironmentCreateReq, db: models.Db):
    environment = models.Environment(
        name=req.name,
        description=req.description,
        location_id=req.location_id,
        environmenttype_id=req.environment_type_id
    )

    db.add(environment)
    db.commit()
