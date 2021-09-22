# Python's Libraries
import logging

# Own's Libraries
from libs.errors.dao_error import DaoError
from models.parent_model import ParentModel
from models.parent_model import ParentCollection


class ParentDao(object):

    def __init__(self, _db, _logger=None):
        self.logger = _logger or logging.getLogger(__name__)
        self.db = _db

    def get_ById(self, _id):
        if _id is None:
            raise DaoError(
                _message="No se proporciono un ID",
                _error=None,
                _logger=self.logger,
            )

        model = ParentModel()
        model.id = _id
        record = self.db.select_One(model)

        return record

    def get_All(self):
        model = ParentModel()
        data_raw = self.db.select_Many(model)

        office_list = ParentCollection()
        office_list.fill(data_raw)

        return office_list
