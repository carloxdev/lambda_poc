
# Third-party Libraries
from unittest import TestCase
from unittest import mock


# Own's Libraries
from test.data.request_examples import DATA_OFFICE_REQUEST
from apps.parent_app import parent_list
from apps.parent_app import parent_retrieve

from libs.sources.rds_source import RdsSource
from models.parent_model import ParentModel
from models.parent_model import ParentCollection


class ParentAppTest(TestCase):

    def test_ListSuccess(self):
        with mock.patch.object(RdsSource, "select_Many") as a:
            collection = ParentCollection()
            collection.append(ParentModel(id=1, description="Testing 1", is_active=True))
            collection.append(ParentModel(id=2, description="Testing 2", is_active=True))
            a.return_value = collection

        response = parent_list(DATA_OFFICE_REQUEST, None)
        print(response)
        self.assertEqual(200, response['statusCode'])

    # def test_RetriveSuccess(self):
    #     with mock.patch.object(RdsSource, "select_One") as a:
    #         a.return_value = ParentModel(id=2, description="Testing", is_active=True)

    #         response = parent_retrieve(DATA_OFFICE_REQUEST, None)
    #         print(response)
    #         self.assertEqual(200, response['statusCode'])
