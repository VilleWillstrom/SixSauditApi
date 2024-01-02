import os
from typing import Optional, Annotated

from fastapi import Depends, Cookie, HTTPException
from fastapi.security import OAuth2PasswordBearer

import models
from Services.auth_sqlalchemy import AuthServ
from dtos.auth import SessionData
from sixsaudit_token.base import AuthResponseHandlerBase
from sixsaudit_token.session import AuthResponseHandlerSession, verifier
from sixsaudit_token.token import Token, AuthResponseHandlerToken

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login', auto_error=False)


# Auto_error needs to be false to use both cookies and headers

class AuthRequiredHandlerBase:  # Middleware baseclass to handle cases where auth is required
    def verify(self, _token: Token, service: AuthServ,
               authorization: Annotated[Optional[str], Depends(oauth_scheme)] = None,
               access_token_cookie: Annotated[Optional[str], Cookie()] = None,
               _cookie: Annotated[Optional[SessionData], Depends(verifier)] = None):
        pass


class AuthRequiredHandlerToken(AuthRequiredHandlerBase):
    def verify(self, _token: Token, service: AuthServ,
               authorization: Annotated[Optional[str], Depends(oauth_scheme)] = None,
               access_token_cookie: Annotated[Optional[str], Cookie()] = None,
               _cookie: Annotated[Optional[SessionData], Depends(verifier)] = None):
        try:

            encoded = None
            if access_token_cookie is not None:
                encoded = access_token_cookie
            else:
                if authorization is not None:
                    encoded = authorization
            if encoded is None:
                raise HTTPException(status_code=401, detail='unauthorized')
            validated = _token.validate(encoded)
            if validated['type'] != 'access':
                raise HTTPException(status_code=401, detail='unauthorized')

            user = service.get_user_by_access_token_identifier(validated['sub'])
            if user is None:
                raise HTTPException(status_code=401, detail='unauthorized')

            return user
        except Exception as e:

            raise HTTPException(status_code=401, detail='unauthorized')


class AuthRequiredHandlerSession(AuthRequiredHandlerBase):
    def verify(self, _token: Token, service: AuthServ,
               authorization: Annotated[Optional[str], Depends(oauth_scheme)] = None,
               access_token_cookie: Annotated[Optional[str], Cookie()] = None,
               _cookie: Annotated[Optional[SessionData], Depends(verifier)] = None):

        try:
            if _cookie is None:
                raise HTTPException(status_code=401, detail='unauthorized')

            user = service.get_user_by_access_token_identifier(_cookie.data)
            if user is None:
                raise HTTPException(status_code=401, detail='unauthorized')
            return user
        except Exception as e:
            raise HTTPException(status_code=401, detail='unauthorized')


def init_auth_res():
    auth_type = os.getenv('AUTH_TYPE')
    if auth_type == 'session':
        return AuthResponseHandlerSession()
    else:
        return AuthResponseHandlerToken()


def init_auth_handler():
    auth_type = os.getenv('AUTH_TYPE')
    if auth_type == 'session':
        return AuthRequiredHandlerSession()
    else:
        return AuthRequiredHandlerToken()


AccountHandler = Annotated[AuthRequiredHandlerBase, Depends(init_auth_handler)]


def get_logged_in_user(_token: Token, service: AuthServ, account_handler: AccountHandler,
                       _cookie: Annotated[Optional[SessionData], Depends(verifier)],
                       authorization: Annotated[Optional[str], Depends(oauth_scheme)] = None,
                       access_token_cookie: Annotated[Optional[str], Cookie()] = None):
    return account_handler.verify(_token, service, authorization, access_token_cookie, _cookie)


def require_admin(_token: Token, service: AuthServ, account_handler: AccountHandler,
                  _cookie: Annotated[Optional[SessionData], Depends(verifier)],
                  authorization: Annotated[Optional[str], Depends(oauth_scheme)] = None,
                  access_token_cookie: Annotated[Optional[str], Cookie()] = None):
    user = account_handler.verify(_token, service, authorization, access_token_cookie, _cookie)
    if user.role != 'admin':
        raise HTTPException(status_code=403, detail='forbidden')
    return user


def require_staff(_token: Token, service: AuthServ, account_handler: AccountHandler,
                  _cookie: Annotated[Optional[SessionData], Depends(verifier)],
                  authorization: Annotated[Optional[str], Depends(oauth_scheme)] = None,
                  access_token_cookie: Annotated[Optional[str], Cookie()] = None):
    user = account_handler.verify(_token, service, authorization, access_token_cookie, _cookie)
    if user.role == 'admin' or user.role == 'staff':
        return user
    raise HTTPException(status_code=403, detail='forbidden')


def get_refresh_token_user(_token: Token, service: AuthServ,
                           authorization: Annotated[Optional[str], Depends(oauth_scheme)] = None,
                           refresh_token_cookie: Annotated[Optional[str], Cookie()] = None):
    try:

        encoded = None
        if refresh_token_cookie is not None:
            encoded = refresh_token_cookie
        else:
            if authorization is not None:
                encoded = authorization
        if encoded is None:
            raise HTTPException(status_code=401, detail='unauthorized')
        validated = _token.validate(encoded)
        if validated['type'] != 'refresh':
            raise HTTPException(status_code=401, detail='unauthorized')

        user = service.get_user_by_refresh_token_identifier(validated['sub'])
        if user is None:
            raise HTTPException(status_code=401, detail='unauthorized')

        return user
    except Exception as e:

        raise HTTPException(status_code=401, detail='unauthorized')


LoggedInUser = Annotated[models.User, Depends(get_logged_in_user)]
Admin = Annotated[models.User, Depends(require_admin)]
Staff = Annotated[models.User, Depends(require_staff)]
AuthRes = Annotated[AuthResponseHandlerBase, Depends(init_auth_res)]
