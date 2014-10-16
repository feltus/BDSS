from unittest import TestCase

from BDSS.common import db_engine, DBSession
from BDSS.models import BaseModel, Job, DataItem
from BDSS.start import start_job

class RunJobTestCase(TestCase):

    def setUp(self):
        BaseModel.metadata.drop_all(bind=db_engine)
        BaseModel.metadata.create_all(bind=db_engine)

        connection = db_engine.connect()
        session = DBSession(bind=connection)

        job_params = {
            'name': 'test job',
            'email': 'watts4@clemson.edu',
            'data_transfer_method': 'sequential_curl',
            'data_destination': 'localhost'
        }
        urls = [
            'http://www.clemson.edu',
            'http://www.google.com'
        ]

        job = Job(**job_params)
        for u in urls:
            d = DataItem(data_url=u)
            job.required_data.append(d)

        session.add(job)
        session.commit()

        session.close()
        connection.close()

    def runTest(self):
        start_job(1)
