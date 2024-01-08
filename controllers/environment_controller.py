from fastapi import APIRouter

import models
from Services.environment_service import EnvironmentServ
from dtos.environment import EnvironmentTypeCreateReq, EnvironmentCreateReq, LocationCreateReq

router = APIRouter(
    prefix='/api/v1/environment',
    tags=['Environment']
)


# Create operation for Location
@router.post('/location')
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
@router.post('/type')
async def create_environment_type(req: EnvironmentTypeCreateReq, db: models.Db):
    # Create a new environment type instance
    environment_type = models.Environmenttype(
        name=req.name
    )

    # Add the environment type to the database and commit the changes
    db.add(environment_type)
    db.commit()


# Create operation for Environment
@router.post('/')
async def create_environment(req: EnvironmentCreateReq, service: EnvironmentServ):
    # Create a new environment instance
    environment = models.Environment(
        name=req.name,
        description=req.description,
        location_id=req.location_id,
        environmenttype_id=req.environmenttype_id
    )

    # Add the environment to the database and commit the changes
    service.add_environment(environment)
    return environment

@router.get('/all')
async def get_all_environments(service: EnvironmentServ):
    environments = service.get_all_environments()
    return environments

@router.get('/all/{location_id}')
async def get_environments_by_location(location_id: int, service: EnvironmentServ):
    environments = service.get_environments_by_location_id(location_id)
    return environments