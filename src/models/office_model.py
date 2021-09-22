# Own's Libraries
from libs.models.base_dynamo import DynamoModel
from libs.models.base_dynamo import DynamoModelCollection


class OfficeModel(DynamoModel):
    __tablename__ = "Offices"

    def __init__(
        self,
        _id=None,
        _name=None,
        _op_key=None
    ):
        self.id = _id
        self.name = _name
        self.op_key = _op_key


class OfficeCollection(DynamoModelCollection):
    __model__ = OfficeModel
