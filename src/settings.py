# Python's Libraries
import os

# Third-party Libraries
from dotenv import load_dotenv

# Own's Libraries
from libs.sources.rds_source import RdsType


load_dotenv()
environment = os.environ.get('APP_ENVIRONMENT')


if environment == "prod":
    RDS_HOSTNAME = "localhost"
    RDS_USER = "dummy"
    RDS_PASSWORD = "dummy"
    RDS_DB_NAME = "testdb"
    RDS_PORT = "3306"
    RDS_TYPE = RdsType.AURORA_REGULAR

elif environment == "dev":
    RDS_DB_NAME = "testdbserverless"
    RDS_SLS_DB_CLUSTER_ARN = "arn:aws:rds:us-east-1:319111408574:cluster:test-aurora-serverless"
    RDS_SLS_SECRETS_STORE_ARN = "arn:aws:secretsmanager:us-east-1:319111408574:secret:rds-db-credentials/cluster-HWWZFVMZHKJ73EZCBBQW3Z3Z4Y/admin-jYNCOa"
    RDS_TYPE = RdsType.AURORA_SERVERLESS

elif environment == "local":
    DYNAMODB_URL = os.environ.get('BTS_APP_DYNAMODB_URL')
    RDS_HOSTNAME = os.environ.get('BTS_APP_RDS_HOSTNAME')
    RDS_USER = os.environ.get('BTS_APP_RDS_USER')
    RDS_PASSWORD = os.environ.get('BTS_APP_RDS_PASSWORD')
    RDS_DB_NAME = os.environ.get('BTS_APP_RDS_DB_NAME')
    RDS_PORT = os.environ.get('BTS_APP_RDS_PORT')
    RDS_TYPE = RdsType.AURORA_REGULAR

else:
    raise NameError("There is no environment configured!")
