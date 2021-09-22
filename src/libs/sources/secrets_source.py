# Python's Libraries
import logging
import json

# Third-party Libraries
import boto3
from botocore.exceptions import ClientError


class SecretsSource(object):

    def __init__(self, _secret_name, _region, _logger=None):
        self.logger = _logger or logging.getLogger(__name__)
        self.secrets = None
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=_region
        )

        try:
            self.logger.info("AWS secrets initializing")
            get_secret_value_response = client.get_secret_value(
                SecretId=_secret_name
            )

            self.logger.info('AWSSecrets initialized sucessfully')
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                self.logger.error("The requested secret " + _secret_name + " was not found")
                raise e
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                self.logger.error("The request was invalid due to: " + str(e))
                raise e
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                self.logger.error("The request had invalid params: " + str(e))
                raise e
            else:
                self.logger.error("The aws secrets had an error: " + str(e))
                raise e

        else:
            # Secrets Manager decrypts the secret value using the associated KMS CMK
            # Depending on whether the secret was a string or binary, only one of these fields will be populated
            self.logger.info(get_secret_value_response)
            if 'SecretString' in get_secret_value_response:
                self.secrets = json.loads(get_secret_value_response['SecretString'])
                self.logger.info('SecretString found in Secrets')

    def get_Secret(self, key):
        if self.secrets and key in self.secrets:
            value = self.secrets[key]
            self.logger.info(f'Secret Value Found For Key {key} : {value[:5]}*******')
            return value
        else:
            self.logger.info(f'Secret Value NOT Found For Key {key}')
            return None
