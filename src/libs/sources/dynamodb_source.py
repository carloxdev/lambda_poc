# Python's Libraries
import logging

# Third-party Libraries
import boto3
from botocore.exceptions import NoCredentialsError

# Own's Libraries
from libs.errors.source_error import SourceError
from libs.errors.source_error import NoRecordFoundError
from libs.errors.source_error import NoRecordsFoundError


class DynamoDBSource(object):

    def __init__(self, _logger=None, _url=None):
        self.logger = _logger or logging.getLogger(__name__)
        self.client = None
        self.url = _url

    def __connect_WithResource(self):
        try:
            if self.url:
                self.client = boto3.resource(
                    'dynamodb',
                    endpoint_url=self.url
                )
            else:
                self.client = boto3.resource('dynamodb')

        except NoCredentialsError as e:
            raise SourceError(
                _message="dynamodb wrong credentials",
                _error=str(e),
                _logger=self.logger
            )

        except Exception as e:
            raise SourceError(
                _message=str(e),
                _logger=self.logger,
                _error=str(e)
            )

    def __connect(self):
        try:
            if self.url:
                self.client = boto3.client(
                    'dynamodb',
                    endpoint_url="http://localhost:8000"
                )

            else:
                self.client = boto3.client(
                    'dynamodb'
                )

        except NoCredentialsError as e:
            raise SourceError(
                _message="dynamodb wrong credentials",
                _error=str(e),
                _logger=self.logger
            )

        except Exception as e:
            raise SourceError(
                _message=str(e),
                _logger=self.logger,
                _error=str(e)
            )

    def select_One(self, _model):
        self.__connect_WithResource()
        filters = _model.get_Dict(_nulls=False)

        try:
            table = self.client.Table(_model.__tablename__)
            response = table.get_item(
                Key=filters
            )

        except Exception as e:
            raise SourceError(
                _message=str(e),
                _error=str(e),
                _logger=self.logger
            )

        data = {}
        if 'Item' in response:
            data = response['Item']

        else:
            raise NoRecordFoundError(
                _message="No record found",
                _logger=self.logger
            )

        return data

    def select_Many(
        self,
        _model,
        _keyconditions,
        _keyconditions_values,
        _attributes_names=None,
        _filters=None,
        _index_name=None,
        _start_key=None,
        _page_size=None
    ):
        if _keyconditions is None or _keyconditions_values is None:
            raise SourceError(
                _message="KeyConditionExpression is missing",
                _error=None,
                _logger=self.logger
            )

        arguments = {}
        arguments['TableName'] = _model.__tablename__
        arguments['KeyConditionExpression'] = _keyconditions
        arguments['ExpressionAttributeValues'] = _keyconditions_values
        arguments['PaginationConfig'] = {
            'PageSize': _page_size,
            'StartingToken': None
        }

        if _index_name:
            arguments['IndexName'] = _index_name

        if _filters:
            arguments['FilterExpression'] = _filters

        if _attributes_names:
            arguments['ExpressionAttributeNames'] = _attributes_names

        if _start_key:
            arguments['ExclusiveStartKey'] = _start_key

        try:
            self.__connect()
            paginator = self.client.get_paginator('query')
            page_iterator = paginator.paginate(**arguments)

            response = {}
            for page in page_iterator:
                response = page
                break

        except Exception as e:
            raise SourceError(
                _message=str(e),
                _error=str(e),
                _logger=self.logger
            )

        if len(response['Items']) == 0:
            raise NoRecordsFoundError(
                _message="No records found",
                _logger=self.logger
            )

        return response
