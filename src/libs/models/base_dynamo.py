# Python's Libraries
import json
from decimal import Decimal


class DynamoModel(object):

    def fill(self, _data_dic, _with_type=False):
        attributes = self.__dict__.keys()

        for key, value in _data_dic.items():
            if key in attributes:
                if _with_type:
                    val = value.values()
                    for i in val:
                        setattr(self, key, i)
                else:
                    setattr(self, key, value)

    def get_Dict(self, _nulls=True):
        dict = {}
        for key, value in self.__dict__.items():
            if _nulls is False:
                if value is None or value == "":
                    continue

            dict[key] = value

        return dict

    def get_Json(self):
        dict = {}
        for key, value in self.__dict__.items():
            val = value
            if isinstance(value, Decimal):
                val = '{0:2f}'.format(value)

            dict[key] = val

        return json.dumps(dict)


class DynamoModelCollection(list):

    def fill(self, _list):
        for item in _list:
            model = self.__model__()
            model.fill(item, _with_type=True)
            self.append(model)

    def get_Json(self):
        data = []
        for item in self:
            dict = {}
            for key, value in item.__dict__.items():
                val = value
                if isinstance(value, Decimal):
                    val = '{0:2f}'.format(value)

                dict[key] = val

            data.append(dict)

        return json.dumps(data)
