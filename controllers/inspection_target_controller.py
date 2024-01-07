from datetime import datetime

from fastapi import APIRouter, HTTPException

import models
from Services.inspection_target_service import InspectionTargetServ
from dtos.target import InspectionTargetCreateReq

router = APIRouter(
    prefix='/api/v1/inspection_target',
    tags=['inspection target']
)


@router.post('/')
async def post_inspection_target(req: InspectionTargetCreateReq, service: InspectionTargetServ):
    # Create operation: Adds a new inspection target.
    timestamp = datetime.now()
    inspection_target = models.Inspectiontarget(
        name=req.name,
        description=req.description,
        createdAt=timestamp,
        environment_id=req.environment_id,
        inspectiontargettype_id=req.inspectiontargettype_id
    )
    # Add the inspection target using the service
    service.add_inspection_target(inspection_target)
    return inspection_target


@router.get('/all')
async def get_inspection_targets(service: InspectionTargetServ):
    # Read operation (get all): Retrieves all inspection targets.
    inspection_targets = service.get_all_inspection_targets()
    return inspection_targets


@router.get('/{inspection_target_id}')
async def get_inspection_target_by_id(inspection_target_id: int, service: InspectionTargetServ):
    # Read operation (get by ID): Retrieves an inspection target by its ID.
    inspection_target = service.get_inspection_target_by_id(inspection_target_id)
    if not inspection_target:
        raise HTTPException(status_code=404, detail="Inspection target not found")
    return inspection_target


@router.put('/{inspection_target_id}')
async def update_inspection_target_by_id(inspection_target_id: int, req: InspectionTargetCreateReq,
                                         service: InspectionTargetServ):
    # Update operation: Modifies an existing inspection target by its ID.
    timestamp = datetime.now()
    updated_inspection_target = models.Inspectiontarget(
        id=inspection_target_id,
        name=req.name,
        description=req.description,
        createdAt=timestamp,
        environment_id=req.environment_id,
        inspectiontargettype_id=req.inspectiontargettype_id
    )
    # Update the inspection target using the service
    service.update_inspection_target_by_id(updated_inspection_target)
    return updated_inspection_target


@router.delete('/{inspection_target_id}')
async def delete_inspection_target_by_id(inspection_target_id: int, service: InspectionTargetServ):
    # Delete operation: Removes an inspection target by its ID.
    inspection_target = service.get_inspection_target_by_id(inspection_target_id)
    if not inspection_target:
        raise HTTPException(status_code=404, detail="Inspection target not found")
    # Delete the inspection target using the service
    service.delete_inspection_target_by_id(inspection_target_id)
    return inspection_target
