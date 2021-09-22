# Python's Libraries
import json

# Third-party Libraries
from unittest import TestCase

# Own's Libraries
from libs.utils.scribe_util import ScribeUtil


class ScribeUtilTest(TestCase):

    def test_Encode_Base64(self):
        data_str = '{"op_key": "BTS", "name": "BTS GROUP - EL PASO, TX.", "id": "3"}'
        data_encode = ScribeUtil.encode_Base64(data_str)
        print(data_encode)

    def test_Decode_Base64(self):
        data_encode = "eyJvcF9rZXkiOiAiQlRTIiwgIm5hbWUiOiAiQlRTIEdST1VQIC0gRUwgUEFTTywgVFguIiwgImlkIjogIjMifQ=="
        data_decode = ScribeUtil.decode_Base64(data_encode)
        print(data_decode)
