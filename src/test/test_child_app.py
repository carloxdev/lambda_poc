
# Third-party Libraries
from unittest import TestCase
from unittest import mock


# Own's Libraries
from test.data.request_examples import DATA_CHILD_REQUEST
from apps.child_app import child_list
from apps.child_app import child_retrieve

from libs.sources.rds_source import RdsSource
from models.child_model import ChildModel
from models.child_model import ChildModelCollection


class ChildAppTest(TestCase):

    def test_ListSuccess(self):
        with mock.patch.object(RdsSource, "select_Many") as a:
            collection = ChildModelCollection()
            collection.append(ChildModel(id=1, description="Child Testing 1", is_active=True))
            collection.append(ChildModel(id=2, description="Child Testing 2", is_active=True))
            a.return_value = collection

        response = child_list(DATA_CHILD_REQUEST, None)
        print(response)
        self.assertEqual(200, response['statusCode'])

    # def test_RetriveSuccess(self):
    #     with mock.patch.object(RdsSource, "select_One") as a:
    #         a.return_value = ChildModel(id=1, description="Testing", is_active=True)

    #         response = child_retrieve(DATA_CHILD_REQUEST, None)
    #         print(response)
    #         self.assertEqual(200, response['statusCode'])
