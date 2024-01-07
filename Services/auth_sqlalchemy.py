import time
import uuid
from typing import Annotated

from fastapi import Depends
from passlib.context import CryptContext

import dtos.auth
import models
from Services.base_service import BaseService
from sixsaudit_token.token import Token

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class AuthService(BaseService):
    def __init__(self, db: models.Db):
        # Initialize AuthService with a database instance by calling BaseService
        super(AuthService, self).__init__(db)

    def register(self, req: dtos.auth.UserRegisterReq):
        # Register a new user in the system
        user = models.User(
            lastName=req.lastName,
            firstName=req.firstName,
            email=req.username,
            password=bcrypt_context.hash(req.password),
            role='student'
        )
        self.db.add(user)
        self.db.commit()
        return user

    def get_user_by_access_token_identifier(self, sub):
        # Retrieve user by access token identifier
        user = self.db.query(models.User).filter(models.User.access_token_identifier == sub).first()
        return user

    def get_user_by_refresh_token_identifier(self, sub):
        # Retrieve user by refresh token identifier
        user = self.db.query(models.User).filter(models.User.refresh_token_identifier == sub).first()
        return user

    def logout(self, sub):
        # Log out a user by updating access and refresh token identifiers to None
        user = self.get_user_by_access_token_identifier(sub)
        user.access_token_identifier = None
        user.refresh_token_identifier = None
        self.db.commit()

    def refresh(self, refreshable_user: models.User, csrf: str, _token: Token):
        # Refresh the access token for a user
        now = time.time()
        access_token_sub = str(uuid.uuid4())
        access_token = _token.create({'type': 'access', 'sub': access_token_sub, 'exp': now + 3600, 'csrf': csrf})
        csrf_token = _token.create({'type': 'csrf', 'sub': csrf, 'exp': None, 'csrf': None})
        refreshable_user.access_token_identifier = access_token_sub
        self.db.commit()

        return {'access_token': access_token,
                'csrf_token': csrf_token,
                'sub': access_token_sub}

    def login(self, username: str, password: str, csrf: str, _token: Token):
        # Log in a user by verifying credentials and generating tokens
        user = self.db.query(models.User).filter(models.User.email == username).first()
        if user is None:
            return None
        valid = bcrypt_context.verify(password, user.password)
        if not valid:
            return None
        now = time.time()
        access_token_sub = str(uuid.uuid4())
        refresh_token_sub = str(uuid.uuid4())
        access_token = _token.create({'type': 'access', 'sub': access_token_sub, 'exp': now + 3600, 'csrf': csrf})
        refresh_token = _token.create(
            {'type': 'refresh', 'sub': refresh_token_sub, 'exp': now + 3600 * 24, 'csrf': None})
        csrf_token = _token.create({'type': 'csrf', 'sub': csrf, 'exp': None, 'csrf': None})

        user.access_token_identifier = access_token_sub
        user.refresh_token_identifier = refresh_token_sub

        self.db.commit()

        return {'access_token': access_token,
                'refresh_token': refresh_token,
                'csrf_token': csrf_token,
                'sub': access_token_sub}

def get_auth_service(db: models.Db):
    # Return an instance of AuthService with a database instance
    return AuthService(db)

AuthServ = Annotated[AuthService, Depends(get_auth_service)]
