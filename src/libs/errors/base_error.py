# Python's Libraries
import logging


class BaseError(Exception):

    def __init__(self, _message, _error=None, _logger=None, _source=None,):
        self.logger = _logger or logging.getLogger(__name__)

        self.message = _message
        self.source = _source
        self.error = _error
        super().__init__(_message)

    def __str__(self):
        value = f'{self.message}'
        if self.error:
            value = f'{value} -> ({self.error})'

        if self.source:
            value = f'in {self.source}: {value}'

        self.logger.error(value)
        return self.message
