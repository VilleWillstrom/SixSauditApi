from fastapi import APIRouter

from Services.user_service import UserServ

router = APIRouter(
    prefix='/api/v1/users',
    tags=['users']
)

@router.get('/all')
async def get_all_users(service: UserServ):
    print('get all starts')
    users = service.get_all_users()
    return {'users': users}

@router.get('/id/{_id}')
async def get_user_by_id(_id: int, service: UserServ):
    user = service.get_user_by_id(_id)
    return user