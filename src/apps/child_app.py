# Python's Libraries

# Third-party Libraries

# Own's Libraries
import settings
from libs.utils.doorman_util import DoormanUtil
from libs.sources.rds_source import RdsSource

from dao.child_dao import ChildDao
from models.child_model import ChildModelSerializer


def child_list(event, context):
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

        child_dao = ChildDao(db, _logger=logger)
        child_list = child_dao.get_All()
        # serializer = ChildModelSerializer(child_list, _many=True)

        return doorman.response_Success(child_list.get_Json())

    except Exception as e:
        return doorman.response_SystemError(str(e))


def child_retrieve(event, context):
    doorman = DoormanUtil(event)

    try:
        id = doorman.get_PathParam("id", True)

        db = RdsSource(
            _database=settings.RDS_DB_NAME,
            _resource_arn=settings.RDS_SLS_DB_CLUSTER_ARN,
            _secret_arn=settings.RDS_SLS_SECRETS_STORE_ARN,
            _db_type=settings.RDS_TYPE
        )

        child_dao = ChildDao(db)
        child_model = child_dao.get_ById(id)

        return doorman.response_Success(
            _message="Solicitud terminada con exito",
            _payload=child_model.get_Json(_relations=True)
        )

    except Exception as e:
        return doorman.response_SystemError(str(e))
