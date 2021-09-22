# Third-party Libraries
from unittest import TestCase
from unittest import mock

# Own's Libraries
from models.client_model import ClientModel
from models.client_model import ClientCollection


class ClientTestModel(TestCase):

    def test_ModelGetDic(self):
        client = ClientModel()
        client.name = "Carlos A."
        client.phone = "12323"
        client.department = "Perrito"

        dict = client.get_Json()
        print(dict)

    def test_CollectionGetJson(self):
        collection = ClientCollection()
        collection.append(ClientModel(_name="Pedro", _position="Gerencia"))
        collection.append(ClientModel(_name="Miguel", _position="Marketing"))

        print(collection.get_Json())
