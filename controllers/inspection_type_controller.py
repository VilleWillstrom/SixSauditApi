from fastapi import APIRouter

import models
from Services.inspection_type_service import InspectionTypeServ
from dtos.inspection_type import InspectionType, InspectionTypeCreateReq

router = APIRouter(
    prefix='/api/v1/inspection_type',
    tags=['inspection type']
)


@router.post('/')
async def post_inspection_type(req: InspectionTypeCreateReq, service: InspectionTypeServ,):
    inspection_type = models.Inspectiontype(
        name=req.name
    )
    service.add_inspection_type(inspection_type)
    return inspection_type


@router.get('/all')
async def get_inspection_types(service: InspectionTypeServ):
    inspection_types = service.get_all_inspection_types()
    return inspection_types


@router.get('/{inspection_type_id}')
async def get_inspection_type_by_id(inspection_type_id: int, service: InspectionTypeServ):
    inspection_type = service.get_inspection_type_by_id(inspection_type_id)
    return inspection_type


@router.put('{inspection_type_id')
async def put_inspection_type_by_id(inspection_type_id: int, req: InspectionTypeCreateReq, service: InspectionTypeServ):
    inspection_type = models.Inspectiontype(
        id=inspection_type_id,
        name=req.name
    )
    service.update_inspection_type_by_id(inspection_type)
    return inspection_type

@router.delete('{inspection_type_id}')
async def delete_inspection_type_by_id(inspection_type_id: int, service: InspectionTypeServ):
    service.delete_inspection_type_by_id(inspection_type_id)
    return True
