from BDSS.common import db_engine, DBSession

from unittest import TestCase

class ModelTestCase(TestCase):

    def setUp(self):
        self.db_connection = db_engine.connect()
        self.db_session = DBSession(bind=self.db_connection)

    def tearDown(self):
        self.db_session.close()
        self.db_connection.close()
