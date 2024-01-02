import unittest

import models


# Unit test is only to test units
# Integration test is testing how i.e. service and model is working together
# Here is mockup classes based on original services, now is not supposed to call models

class UserServiceEmptyOk:
    def get_all_users(self):
        return []


'''
    id = Column(INTEGER(11), primary_key=True)
    firstName = Column(String(45), nullable=False)
    lastName = Column(String(45), nullable=False)
    email = Column(String(45), nullable=False, unique=True)
    role = Column(String(45), nullable=False)
    password = Column(String(255), nullable=False)
    access_token_identifier = Column(String(45))
    refresh_token_identifier = Column(String(45))
'''


class UserServiceNotEmptyOk:
    def get_all_users(self):
        return [models.User(id=1, firstName='John', lastName='Doe', email='not@real.com', role='admin',
                            password='asdfgh')]


class TestUserService(unittest.TestCase):
    def setUp(self) -> None:
        self.emptyok = UserServiceEmptyOk()
        self.notemptyok = UserServiceNotEmptyOk()

    def test_empty_ok(self):
        users = self.emptyok.get_all_users()
        self.assertEqual(users, [])

    def test_not_empty_ok(self):
        users = self.notemptyok.get_all_users()
        # self.assertEqual(len(users), 1)
        expected = models.User()
        self.assertEqual(users[0], expected)
