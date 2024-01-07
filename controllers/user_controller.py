from fastapi import APIRouter

from Services.user_service import UserServ

router = APIRouter(
    prefix='/api/v1/users',
    tags=['users']
)

# Read operation (get all)
@router.get('/all')
async def get_all_users(service: UserServ):
    print('get all starts')
    # Retrieve all users using the service
    users = service.get_all_users()
    return {'users': users}

# Read operation (get by ID)
@router.get('/id/{_id}')
async def get_user_by_id(_id: int, service: UserServ):
    # Retrieve a user by their ID using the service
    user = service.get_user_by_id(_id)
    return user
