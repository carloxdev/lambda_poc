# Python's Libraries
import os
# import logging
import logging.config
import json

# Third-party Libraries
import yaml

# Own's Libraries
from libs.errors.util_error import UtilError


class DoormanUtil(object):

    def __init__(self, _request, _logger=None):
        self.logger = _logger or logging.getLogger(__name__)
        self.request = _request

    def create_Logger(self):
        # src_path = os.path.dirname(os.path.abspath(__file__), os.pardir, os.pardir)
        config_file = os.path.abspath(
            os.path.join(
                os.path.abspath(__file__),
                os.pardir, os.pardir, os.pardir,
                "configlog.yaml"
            )
        )

        with open(config_file, 'r') as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)

        logger = logging.getLogger(__name__)
        self.logger = logger
        return logger

    def get_BodyParam(self, _param_name, _is_required=False):
        if 'body' not in self.request:
            raise UtilError(
                _message="There is no body in request data",
                _error=None,
                _logger=self.logger,
            )

        if self.request['body'] is None:
            raise UtilError(
                _message="The body node is null",
                _error=None,
                _logger=self.logger,
            )

        try:
            body = json.loads(self.request['body'])
            param_value = None

            if body[_param_name] is None or \
                    body[_param_name] == "":
                if _is_required:
                    raise NameError(
                        f"Value of {_param_name} is missing"
                    )

                param_value = None

            else:
                param_value = body[_param_name]

            return param_value

        except Exception as e:
            raise UtilError(
                _message=str(e),
                _error=str(e),
                _logger=self.logger
            )

    def get_QueryParam(self, _param_name, _is_required=False):
        if 'queryStringParameters' not in self.request:
            if _is_required:
                raise UtilError(
                    _message="There is no queryStringParameters in request data",
                    _error=None,
                    _logger=self.logger,
                )
            else:
                return None

        if self.request['queryStringParameters'] is None:
            if _is_required:
                raise UtilError(
                    _message="The queryStringParameters node is null",
                    _error=None,
                    _logger=self.logger,
                )
            else:
                return None

        if _param_name not in self.request['queryStringParameters']:
            if _is_required:
                raise UtilError(
                    _message=f"There is no {_param_name} in queryStringParameters",
                    _error=None,
                    _logger=self.logger,
                )
            else:
                return None

        try:
            query_parameters = self.request['queryStringParameters']
            param_value = None

            if query_parameters[_param_name] is None or \
                    query_parameters[_param_name] == "":
                if _is_required:
                    raise UtilError(
                        _message=f"Value of {_param_name} is missing",
                        _error=None,
                        _logger=self.logger,
                    )

                param_value = None

            else:
                param_value = query_parameters[_param_name]

            return param_value

        except Exception as e:
            raise UtilError(
                _message=str(e),
                _error=str(e),
                _logger=self.logger
            )

    def get_PathParam(self, _param_name, _is_required=False):
        if 'pathParameters' not in self.request:
            raise UtilError(
                _message="El request no incluyo datos en pathParameters",
                _error=None,
                _logger=self.logger,
            )

        if self.request['pathParameters'] is None:
            raise UtilError(
                _message="The pathParameters node is null",
                _error=None,
                _logger=self.logger,
            )

        try:
            path_parameters = self.request['pathParameters']
            param_value = None

            if path_parameters[_param_name] is None or \
                    path_parameters[_param_name] == "":
                if _is_required:
                    raise UtilError(
                        _message=f"Value of {_param_name} is missing",
                        _error=None,
                        _logger=self.logger,
                    )

                param_value = None

            else:
                param_value = path_parameters[_param_name]

            return param_value

        except Exception as e:
            raise UtilError(
                _message=str(e),
                _error=str(e),
                _logger=self.logger
            )

    def response_Success(self, _payload):
        response = {
            'isBase64Encoded': False,
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': "Content-Type,Authorization,x-apigateway-header,X-Amz-Date,X-Api-Key,X-Amz-Security-Token",
                'Access-Control-Allow-Methods': "GET, POST, PATCH, OPTIONS, DELETE"
            },
            'body': json.dumps(_payload)
        }

        self.logger.info(response)
        return response

    def response_UserError(self, _message, _code=400):
        response = {
            'isBase64Encoded': False,
            'statusCode': _code,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': "Content-Type,Authorization,x-apigateway-header,X-Amz-Date,X-Api-Key,X-Amz-Security-Token",
                'Access-Control-Allow-Methods': "GET, POST, PATCH, OPTIONS, DELETE"
            },
            'body': json.dumps({
                'message': _message
            }, ensure_ascii=False)
        }

        self.logger.error(response)
        return response

    def response_SystemError(self, _message, _code=503):
        response = {
            'isBase64Encoded': False,
            'statusCode': _code,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': "Content-Type,Authorization,x-apigateway-header,X-Amz-Date,X-Api-Key,X-Amz-Security-Token",
                'Access-Control-Allow-Methods': "GET, POST, PATCH, OPTIONS, DELETE"
            },
            'body': json.dumps({
                'message': _message
            }, ensure_ascii=False)
        }

        self.logger.error(response)
        return response

    def response_Forbidden(self, _message, _code=403):
        response = {
            'isBase64Encoded': False,
            'statusCode': _code,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': "Content-Type,Authorization,x-apigateway-header,X-Amz-Date,X-Api-Key,X-Amz-Security-Token",
                'Access-Control-Allow-Methods': "GET, POST, PATCH, OPTIONS, DELETE"
            },
            'body': json.dumps({
                'message': _message
            })
        }

        self.logger.info(response)
        return response
