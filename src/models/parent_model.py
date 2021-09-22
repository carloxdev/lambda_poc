
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


class ParentModel(Base, RdsModel):
    __tablename__ = "parent"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(100))
    is_active = Column(Boolean)


class ParentCollection(RdsModelCollection):
    pass
