from unittest import TestCase, TestSuite, TextTestRunner

from BDSS.data_transfer.models import DataItem

from .common import ModelTestCase

class DataItemValidateUrlTestCase(ModelTestCase):

    def runTest(self):
        item = DataItem(data_url='file:///Users/nwatts/Desktop/test.txt', checksum='abc')

        self.db_session.add(item)
        self.db_session.commit()


data_item_test_suite = TestSuite()

data_item_test_suite.addTest(DataItemValidateUrlTestCase())
