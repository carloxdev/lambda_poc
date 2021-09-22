
# Third-party Libraries
from sqlalchemy import create_engine

# Own's Libraries
from libs.sources.sqlalchemy_base import Base
from libs.sources.rds_source import RdsType
from libs.errors.source_error import SourceError

from models.child_model import ChildModel
from models.parent_model import ParentModel

import settings


engine = None

print("Conectando con DB .... ")
if settings.RDS_TYPE == RdsType.AURORA_REGULAR:
    engine = create_engine(
        f'mysql+pymysql://{settings.RDS_USER}:{settings.RDS_PASSWORD}@{settings.RDS_HOSTNAME}:{settings.RDS_PORT}/{settings.RDS_DB_NAME}'
    )

elif settings.RDS_TYPE == RdsType.AURORA_SERVERLESS:
    engine = create_engine(
        f'mysql+auroradataapi://:@/{settings.RDS_DB_NAME}',
        echo=True,
        connect_args=dict(aurora_cluster_arn=settings.RDS_SLS_DB_CLUSTER_ARN, secret_arn=settings.RDS_SLS_SECRETS_STORE_ARN)
    )

else:
    raise SourceError("No se definio un tipo de RDS valido!")

print("Modificando DB .... ")
Base.metadata.create_all(engine)

print("Modificacion Exitosa")
