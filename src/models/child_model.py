
# Third-party Libraries
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import Float
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

# Own's Libraries
from libs.sources.sqlalchemy_base import Base
from libs.models.base_rds import RdsModel
from libs.models.base_rds import RdsModelCollection
from libs.models.base_rds import RdsModelSerializer

from models.parent_model import ParentModel


class ChildModel(Base, RdsModel):
    __tablename__ = "child"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(100))
    is_active = Column(Boolean)
    parent_id = Column(Integer, ForeignKey('parent.id'))
    parent = relationship(
        ParentModel,
        foreign_keys=[parent_id],
        backref="child_record"
    )


class ChildModelCollection(RdsModelCollection):
    pass


class ChildModelSerializer(RdsModelSerializer):
    list_attrs = [
        'id',
        'description'
    ]
