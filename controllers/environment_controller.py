from fastapi import APIRouter

import models
from dtos.environment import EnvironmentTypeCreateReq, EnvironmentCreateReq, LocationCreateReq

router = APIRouter()

# Create operation for Location
@router.post('/api/v1/location')
async def create_location(req: LocationCreateReq, db: models.Db):
    # Create a new location instance
    location = models.Location(
        name=req.name,
        address=req.address,
        zip_code=req.zip_code
    )

    # Add the location to the database and commit the changes
    db.add(location)
    db.commit()

# Create operation for EnvironmentType
@router.post('/api/v1/environment_type')
async def create_environment_type(req: EnvironmentTypeCreateReq, db: models.Db):
    # Create a new environment type instance
    environment_type = models.Environmenttype(
        name=req.name
    )

    # Add the environment type to the database and commit the changes
    db.add(environment_type)
    db.commit()

# Create operation for Environment
@router.post('/api/v1/environment')
async def create_environment(req: EnvironmentCreateReq, db: models.Db):
    # Create a new environment instance
    environment = models.Environment(
        name=req.name,
        description=req.description,
        location_id=req.location_id,
        environmenttype_id=req.environment_type_id
    )

    # Add the environment to the database and commit the changes
    db.add(environment)
    db.commit()
