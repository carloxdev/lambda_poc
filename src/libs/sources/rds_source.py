# Python's Libraries
import logging
import inspect

# Third-party Libraries
from sqlalchemy import create_engine
from sqlalchemy import desc
from sqlalchemy import asc

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
# from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy.sql.sqltypes import Enum

from sqlalchemy_pagination import paginate

# Own's Libraries
from libs.errors.source_error import SourceError
from libs.errors.source_error import NoRecordFoundError
from libs.errors.source_error import MultipleRecordsFoundError


class RdsType(Enum):
    AURORA_REGULAR = "AURORA_REGULAR"
    AURORA_SERVERLESS = "AURORA_SERVERLESS"


class RdsSource(object):
    """Object with methods that help with the DB operations"""

    def __init__(
        self,
        _database,
        _user=None,
        _password=None,
        _host=None,
        _port=3306,
        _db_type=None,
        _resource_arn=None,
        _secret_arn=None,
        _logger=None
    ):
        if _db_type == RdsType.AURORA_REGULAR:
            self.engine = create_engine(
                f'mysql+pymysql://{_user}:{_password}@{_host}:{_port}/{_database}'
            )

        elif _db_type == RdsType.AURORA_SERVERLESS:
            self.engine = create_engine(
                f'mysql+auroradataapi://:@/{_database}',
                echo=True,
                connect_args=dict(aurora_cluster_arn=_resource_arn, secret_arn=_secret_arn)
            )

        else:
            raise SourceError("No RdsType was defined!")

        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.records_per_page = 20
        self.logger = _logger or logging.getLogger(__name__)

    def select_One(self, _model):
        """Search for a record from the attributes of a model

        :param _model: Object of type Model to be search
        :type _model: Model
        :raises SourceError: When fail some validation
        :raises NoRecordFoundError: When the record is not found
        :raises MultipleRecordsFoundError: When more than one record is found
        :return: Object of type Model
        :rtype: Model
        """
        self.logger.info(
            f'... Searching in table: {_model.__table__}'
        )

        filters = _model.get_Dict(_nulls=False)

        if bool(filters) is False:
            raise SourceError(
                "... No value was specified in any attribute."
            )

        try:
            query = self.session.query(_model.__class__)
            for key in filters.keys():
                query = query.filter(
                    getattr(_model.__class__, key) == filters[key]
                )

            record = query.one()

            self.logger.info('... Record found!')
            return record

        except NoResultFound:
            msg = f"No record found in {_model.__class__.__name__}"
            raise NoRecordFoundError(
                _message=msg,
                _error=msg,
            )

        except MultipleResultsFound:
            msg = f"There is more than one record in {_model.__class__.__name__}."
            raise MultipleRecordsFoundError(
                _message=msg,
                _error=msg,
            )

        except Exception as e:
            self.session.rollback()
            msg = f"{str(e)}"
            raise SourceError(
                _message=msg,
                _error=msg,
            )

    def select_Many(
        self,
        _model,
        _custom_filters=None,
        _order_column=None,
        _arrange="asc",
        _page=1
    ):
        self.logger.info(f'... Searching in table: {_model.__table__}')
        try:
            if _custom_filters is not None:
                query = self.session.query(_model.__class__)
                query = query.filter(_custom_filters)

            else:
                filters = _model.get_Dict(_nulls=False)

                if bool(filters) is False:
                    query = self.session.query(_model.__class__)

                else:
                    query = self.session.query(_model.__class__)
                    for key in filters.keys():
                        query = query.filter(
                            getattr(_model.__class__, key) == filters[key]
                        )

            records = None

            if _order_column:
                page = paginate(
                    query.order_by(eval(f"{_arrange}({_order_column})")),
                    _page,
                    self.records_per_page
                )

            else:
                page = paginate(
                    query,
                    _page,
                    self.records_per_page
                )
                records = page.items

        except Exception as e:
            self.session.rollback()
            raise SourceError(
                _message=str(e),
                _source="RdsSource.select_Many"
            )

        qty_records = len(records)
        if qty_records == 0:
            msg = f'No records found in {_model.__class__.__name__}'
            raise NoRecordFoundError(
                _message=msg,
                _error=msg,
                _source="RdsSource.select_Many"
            )

        self.logger.info(f'{qty_records} records found')

        return records
