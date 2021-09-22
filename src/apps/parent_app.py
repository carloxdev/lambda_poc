# Python's Libraries

# Third-party Libraries

# Own's Libraries
from json import decoder
import settings
from libs.utils.doorman_util import DoormanUtil
from libs.sources.rds_source import RdsSource

from dao.parent_dao import ParentDao


def parent_list(event, context):
    doorman = DoormanUtil(event)

    try:
        logger = doorman.create_Logger()
        db = RdsSource(
            _user=settings.RDS_USER,
            _password=settings.RDS_PASSWORD,
            _host=settings.RDS_HOSTNAME,
            _port=settings.RDS_PORT,
            _database=settings.RDS_DB_NAME,
            _db_type=settings.RDS_TYPE,
            _logger=logger
        )

        parent_dao = ParentDao(db, _logger=logger)
        parent_list = parent_dao.get_All()

        return doorman.response_Success(parent_list.get_Json())

    except Exception as e:
        return doorman.response_SystemError(str(e))


def parent_retrieve(event, context):
    doorman = DoormanUtil(event)

    try:
        id = doorman.get_PathParam("id", True)

        db = RdsSource(
            _user=settings.RDS_USER,
            _password=settings.RDS_PASSWORD,
            _host=settings.RDS_HOSTNAME,
            _port=settings.RDS_PORT,
            _database=settings.RDS_DB_NAME,
            _db_type=settings.RDS_TYPE
        )

        parent_dao = ParentDao(db)
        parent_model = parent_dao.get_ById(id)

        return doorman.response_Success(
            _message="Solicitud terminada con exito",
            _payload=parent_model.get_Json()
        )

    except Exception as e:
        return doorman.response_SystemError(str(e))
