# Third-party Libraries
from unittest import TestCase

from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr


# Own's Libraries
import settings
from libs.sources.dynamodb_source import DynamoDBSource
from models.office_model import OfficeModel


class DynamodbSourceTest(TestCase):

    def test_SelectMany_All(self):
        db = DynamoDBSource(_url=settings.DYNAMODB_URL)
        model = OfficeModel()
        conditions = Key('id').eq("24")
        response = db.select_Many(
            model,
            conditions
        )

        print(response)
        self.assertTrue(isinstance(response, list))

    def test_SelectMany_WithContain(self):
        db = DynamoDBSource(_url=settings.DYNAMODB_URL)
        model = OfficeModel()
        index_name = "op-index"
        conditions = Key('op_key').eq("BTS")
        filters = Attr('name').contains("LAREDO")
        response = db.select_Many(
            model,
            conditions,
            _filters=filters,
            _index_name=index_name
        )

        print(response)
        self.assertTrue(isinstance(response, list))
