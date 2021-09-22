# Third-party Libraries

# Own's Libraries
import settings
from libs.utils.doorman_util import DoormanUtil
from libs.sources.dynamodb_source import DynamoDBSource
from libs.errors.source_error import NoRecordFoundError

from dao.office_dao import OfficeDao


def office_list(event, context):
    doorman = DoormanUtil(event)
    logger = doorman.create_Logger()

    try:
        name = doorman.get_QueryParam("name")
        db = DynamoDBSource(
            _url=settings.DYNAMODB_URL,
            _logger=logger
        )
        office_dao = OfficeDao(db, _logger=logger)
        office_list = office_dao.get_All(_name=name)

        return doorman.response_Success(
            _message="Solicitud terminada con exito",
            _payload=office_list.get_Json()
        )

    except Exception as e:
        return doorman.response_SystemError(str(e))
