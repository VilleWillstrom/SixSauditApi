import unittest

from starlette.testclient import TestClient

from main import app


class TestMain(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def test_get_all_users(self):
        res = self.client.get('/api/v1/users/')
        self.assertEqual(res.status_code, 200)
