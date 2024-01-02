import unittest

from sqlalchemy.orm import close_all_sessions

import models


# This one creates fresh db for each test
class TestEnvironmentTypeModelDelete(unittest.TestCase):
    def setUp(self) -> None:
        models.metadata.create_all(bind=models.engine)
        self.db = models.Db(bind=models.engine)

        et = models.Environmenttype(name='asdfgh')
        self.db.add(et)
        self.db.commit()

    def test_delete(self):
        et = self.db.query(models.Environmenttype).filter(models.Environmenttype.id == 1).first()
        self.db.delete(et)

        ets = self.db.query(models.Environmenttype).all()
        self.assertEqual(ets, [])

    def tearDown(self) -> None:
        close_all_sessions()
        models.metadata.drop_all(bind=models.engine)


class TestEnvironmentTypeModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        models.metadata.create_all(bind=models.engine)  # Creating new database for all tests
        cls.db = models.Db(bind=models.engine)

    def _get_by_id(self, _id: int) -> models.Environmenttype:
        return self.db.query(models.Environmenttype).filter(models.Environmenttype.id == _id).first()

    def test_create_environmenttype(self):
        environment_type = models.Environmenttype(name='Laboratory')
        self.db.add(environment_type)
        self.db.commit()

        self.assertEqual(environment_type.id, 1)  # in fresh relation db first inserted id is 1
        self.assertEqual(environment_type.name, 'Laboratory')  # name has to match to the one provided above

    def test_get_all(self):
        environment_types = self.db.query(models.Environmenttype).all()
        self.assertEqual(len(environment_types), 1)

    def test_get_by_id_ok(self):
        et = self.db.query(models.Environmenttype).filter(models.Environmenttype.id == 1).first()
        self.assertEqual(et.id, 1)

    def test_get_by_id_none(self):
        et = self.db.query(models.Environmenttype).filter(models.Environmenttype.id == 2).first()
        self.assertEqual(et, None)

    def test_update_by_id(self):
        self.db.query(models.Environmenttype).filter(models.Environmenttype.id == 1).update({'name': 'Updated'})
        self.db.commit()
        et = self._get_by_id(1)
        self.assertEqual(et.name, 'Updated')

    '''def test_delete_by_id(self):
        et = self._get_by_id(1)
        self.db.delete(et)
        self.db.commit()
        et.self._get_by_id(1)
        self.assertEqual(et, None)'''

    @classmethod
    def tearDownClass(cls) -> None:
        close_all_sessions()
        models.metadata.drop_all(bind=models.engine)  # Dropping test db
