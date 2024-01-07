from fastapi import APIRouter

import models
from Services.location_service import LocationServ
from dtos.location import LocationCreateReq, Location

router = APIRouter(
    prefix='/api/v1/location',
    tags=['location']
)

# Create operation
@router.post('/')
async def post_location(req: LocationCreateReq, service: LocationServ):
    # Create a new Location object
    location = models.Location(
        name=req.name,
        address=req.address,
        zip_code=req.zip_code
    )
    # Add the location using the service
    service.add_location(location)
    return location

# Read operation (get all)
@router.get('/all')
async def get_locations(service: LocationServ):
    # Retrieve all locations using the service
    locations = service.get_all_locations()
    return locations

# Read operation (get by ID)
@router.get('/{location_id}')
async def get_location_by_id(location_id: int, service: LocationServ):
    # Retrieve a location by its ID using the service
    location = service.get_location_by_id(location_id)
    return location

# Update operation
@router.put('/{location_id}')
async def update_location_by_id(location_id: int, req: LocationCreateReq, service: LocationServ):
    # Create an updated Location object
    location = models.Location(
        id=location_id,
        name=req.name,
        address=req.address,
        zip_code=req.zip_code
    )
    # Update the location using the service
    service.update_location_by_id(location)
    return location

# Delete operation
@router.delete('/{location_id}')
async def delete_location_by_id(location_id: int, service: LocationServ):
    # Delete a location by its ID using the service
    service.delete_location_by_id(location_id)
    return True
