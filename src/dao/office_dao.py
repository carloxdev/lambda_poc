# Python's Libraries
import logging

# Third-party Libraries
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr

# Own's Libraries
from models.office_model import OfficeModel
from models.office_model import OfficeCollection


class OfficeDao(object):

    def __init__(self, _db, _logger=None):
        self.logger = _logger or logging.getLogger(__name__)
        self.db = _db

    def get_All(self, _name=None):
        filters = {}
        index_name = "op-index"
        conditions = Key('op_key').eq("BTS")
        if _name:
            filters = Attr('name').contains(_name)

        model = OfficeModel()
        data_raw = self.db.select_Many(
            model,
            conditions,
            _filters=filters,
            _index_name=index_name
        )

        office_list = OfficeCollection()
        office_list.fill(data_raw)

        return office_list
