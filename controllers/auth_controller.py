import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import Response

import models
import sixsaudit_token.token
from Services.auth_sqlalchemy import AuthServ
from dependencies import LoggedInUser, AuthRes, get_refresh_token_user, Admin, Staff
from dtos.auth import UserRegisterReq, UserRegisterRes, UserLoginRes, UserAccountRes, SessionData
from sixsaudit_token.session import backend, cookie, verifier

router = APIRouter(
    tags=['auth'],
    prefix='/api/v1/auth'
)

LoginForm = Annotated[OAuth2PasswordRequestForm, Depends()]  # Has to be at least empty Depends()


@router.get('/account/admin', dependencies=[Depends(cookie)], response_model=UserAccountRes)
async def get_admin(account: Admin):
    return account


@router.get('/account/staff', dependencies=[Depends(cookie)], response_model=UserAccountRes)
async def get_staff(account: Staff):
    return account


@router.get('/account', dependencies=[Depends(cookie)], response_model=UserAccountRes)
async def get_account(account: LoggedInUser):
    return account


# version number is suggested to keep here, so there can be several versions running at same time
@router.post('/register', response_model=UserRegisterRes)
async def register(req: UserRegisterReq, service: AuthServ):
    user = service.register(req)
    return {'username': user.email, 'firstName': user.firstName, 'lastName': user.lastName}


@router.post('/login')
async def login(service: AuthServ, login_form: LoginForm, _token: sixsaudit_token.token.Token, res: Response,
                res_handler: AuthRes):
    csrf = str(uuid.uuid4())
    tokens = service.login(login_form.username, login_form.password, csrf, _token)
    if tokens is None:
        raise HTTPException(status_code=404, detail='user not found')

    return await res_handler.send(res, tokens['access_token'], tokens['refresh_token'],
                                  tokens['csrf_token'], tokens['sub'])


@router.post('/refresh')
async def refresh(service: AuthServ, _token: sixsaudit_token.token.Token, res: Response,
                  refreshable_account: Annotated[models.User,
                  Depends(get_refresh_token_user)]):
    csrf = str(uuid.uuid4())
    tokens = service.refresh(refreshable_account, csrf, _token)
    res.set_cookie('access_token_cookie', tokens['access_token'], httponly=True, secure=True)
    res.set_cookie('csrf_token_cookie', tokens['csrf_token'], httponly=True, secure=True)
    return tokens


@router.post('/logout')
async def logout(service: AuthServ, res: Response, session_id: Annotated[uuid.UUID, Depends(cookie)],
                 account: LoggedInUser, res_handler: AuthRes):
    # Using annotated/type alias to dodge key order issue - making it non default parameter

    service.logout(account.access_token_identifier)
    await res_handler.logout(session_id, res)
    return True
