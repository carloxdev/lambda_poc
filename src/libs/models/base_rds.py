# Python's Libraries
import json
from datetime import datetime

# Third-party Libraries
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm.collections import InstrumentedList


class RdsModel(object):

    def backref_ToDic(self, _value, _signer=None):
        data = []
        for item in _value:
            item_dict = item.get_Dict(
                _relations=False,
                _signer=_signer
            )
            data.append(item_dict)

        return data

    def get_Dict(
        self,
        _nulls=True,
        _primaries=True,
        _relations=False,
        _backref=False,
        _except_rel=[],
        _signer=None
    ):
        data = {}

        for attr, column in self.__mapper__.c.items():
            if _primaries is False and column.primary_key:
                continue

            column_value = getattr(self, attr)
            if _nulls is False and column_value is None:
                continue

            data[column.key] = column_value

        if _relations:
            for attr, relation in self.__mapper__.relationships.items():

                value = getattr(self, attr)

                if value is None and _nulls:
                    data[relation.key] = None
                    continue

                if relation.key in _except_rel:
                    continue

                if type(value) == InstrumentedList:
                    if _backref is False:
                        continue

                    if relation.key in _except_rel:
                        continue

                    if value:
                        data[relation.key] = self.backref_ToDic(
                            _value=value,
                            _signer=_signer
                        )

                    else:
                        data[relation.key] = value

                else:
                    data[relation.key] = value.get_Dict(
                        _nulls=_nulls,
                        _primaries=_primaries,
                        _relations=_relations,
                        _backref=_backref,
                        _except_rel=_except_rel,
                        _signer=_signer
                    )

        return data

    def get_Json(
        self,
        _relations=False,
        _backref=False,
        _except_rel=[],
        _signer=None
    ):

        def extended_encoder(x):
            if isinstance(x, datetime):
                return x.isoformat()

        return json.dumps(
            self.get_Dict(
                _relations=_relations,
                _backref=_backref,
                _except_rel=_except_rel,
                _signer=_signer
            ),
            default=extended_encoder
        )


class RdsModelCollection(list):

    def fill(self, _list):
        self.extend(_list)

    def get_Json(self):
        data = []
        for item in self:
            data.append(item.get_Dict())

        return json.dumps(data)


class RdsModelSerializer(object):

    def __init__(self, _data=None, _many=False):
        self.data = _data
        self.many = _many

        if hasattr(self, "list_attrs") is False:
            raise NameError("list_attrs is not defined")

    def __get_ItemDict(self, _item):
        data = {}
        for attr, column in self.__mapper__.c.items():
            import pdb; pdb.set_trace()
            pass

        return data

    def get_Dict(self):
        if self.many:
            list = []
            for dta in self.data:
                list.append(self.__get_ItemDict(dta))

            return list
        else:
            return self.__get_ItemDict(self.data)

    def get_Json(self):
        json_data = json.dumps(self.get_Dict())
        return json_data
