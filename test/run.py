from unittest import TestCase

from BDSS.common import db_engine, DBSession
from BDSS.models import BaseModel, Job, DataItem
from BDSS.background import start_job

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
            'ftp://130.14.250.7/sra/sra-instant/reads/ByRun/sra/SRR/SRR039/SRR039884/SRR039884.sra',
            'ftp://130.14.250.7/sra/sra-instant/reads/ByRun/sra/SRR/SRR039/SRR039885/SRR039885.sra',
            'ftp://130.14.250.7/sra/sra-instant/reads/ByRun/sra/SRR/SRR058/SRR058526/SRR058526.sra',
            'ftp://130.14.250.7/sra/sra-instant/reads/ByRun/sra/SRR/SRR058/SRR058527/SRR058527.sra',
            'ftp://130.14.250.7/sra/sra-instant/reads/ByRun/sra/SRR/SRR058/SRR058528/SRR058528.sra'
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
        connection = db_engine.connect()
        session = DBSession(bind=connection)
        job = session.query(Job).first()
        start_job(job)
        session.close()
        connection.close()
