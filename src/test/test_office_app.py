
# Third-party Libraries
from unittest import TestCase
from unittest import mock


# Own's Libraries
from test.data.request_office_all import REQUEST_OFFICE_ALL
from apps.office_app import office_list

from libs.sources.dynamodb_source import DynamoDBSource


class OfficeAppTest(TestCase):

    def test_ListSuccess(self):
        with mock.patch.object(DynamoDBSource, "select_Many") as a:
            a.return_value = [
                {
                    'department': 'Marketing 2',
                    'id': 'EI8312',
                    'name': 'Jorge Jimenez',
                    'phone': 892123122
                }, {
                    'department': 'Marketing 2',
                    'id': 'ID25101',
                    'name': 'Carlos A. Martinez',
                    'position': 'Development'
                }, {
                    'department': 'Marketing 2',
                    'id': 'RF231',
                    'name': 'Gabriela Rivero',
                    'position': 'Gerencia'
                }
            ]

            response = office_list(REQUEST_OFFICE_ALL, None)
            print(response)
            self.assertEqual(200, response['statusCode'])
