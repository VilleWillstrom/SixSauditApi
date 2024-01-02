from typing import Annotated

from fastapi import Depends

import models
from Services.base_service import BaseService


class UserService(BaseService):
    def __init__(self, db: models.Db):
        super(UserService, self).__init__(db)

    def get_all_users(self):
        users = self.db.query(models.User).all()
        return users

    def get_user_by_id(self, _id):
        user = self.db.query(models.User).get(_id)
        return user


def init_user_service(db: models.Db):
    return UserService(db)


UserServ = Annotated[UserService, Depends(init_user_service)]
