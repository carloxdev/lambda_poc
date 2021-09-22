# Third-party Libraries
from unittest import TestCase
from unittest import mock

# Own's Libraries
from libs.sources.dynamodb_source import DynamoDBSource
from libs.errors.source_error import SourceError
from libs.errors.source_error import NoRecordsFoundError

from dao.office_dao import OfficeDao
from models.office_model import OfficeCollection


class OfficeDaoTest(TestCase):

    def test_GetAll_Sucess(self):
        with mock.patch.object(DynamoDBSource, "select_Many") as a:
            a.return_value = [
                {
                    'id': 'EI8312',
                    'name': 'CDMX North',
                    'op_key': 'BTS'
                },
                {
                    'id': 'ID25101',
                    'name': 'CDMX South',
                    'op_key': 'BTS'
                },
                {
                    'id': 'RF231',
                    'name': 'CDMX West',
                    'op_key': 'BTS'
                }
            ]

            db = DynamoDBSource()
            office_dao = OfficeDao(db)
            office_list = office_dao.get_All()

            self.assertEqual(isinstance(office_list, OfficeCollection), True)

    def test_GetAll_NoRecords(self):
        error_mock = mock.Mock()
        error_mock.side_effect = NoRecordsFoundError("No records found")

        with mock.patch.object(DynamoDBSource, "select_Many", error_mock):
            db = DynamoDBSource()
            office_dao = OfficeDao(db)

            with self.assertRaises(NoRecordsFoundError):
                office_dao.get_All()

    def test_GetAll_Fail(self):
        error_mock = mock.Mock()
        error_mock.side_effect = SourceError("dynamodb wrong credentials")

        with mock.patch.object(DynamoDBSource, "select_Many", error_mock):

            db = DynamoDBSource()
            office_dao = OfficeDao(db)

            with self.assertRaises(SourceError):
                office_dao.get_All()
