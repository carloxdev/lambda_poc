# Python's Libraries
from decimal import Decimal

# Third-party Libraries
from unittest import TestCase
from unittest import mock

# Own's Libraries
from test.data.request_examples import DATA_CLIENT_REQUEST
from apps.client_app import client_list
from apps.client_app import client_retrieve

from libs.sources.dynamodb_source import DynamoDBSource


class ClientControllerTest(TestCase):

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

            response = client_list(DATA_CLIENT_REQUEST, None)
            print(response)
            self.assertEqual(200, response['statusCode'])

    def test_RetriveSuccess(self):
        with mock.patch.object(DynamoDBSource, "select_One") as a:
            a.return_value = {
                'department': 'Marketing',
                'id': 'IK2123',
                'name': 'Pepe Gomez',
                'position': 'Supervisor',
                'phone': 829212312
            }

            response = client_retrieve(DATA_CLIENT_REQUEST, None)
            print(response)
            self.assertEqual(200, response['statusCode'])
