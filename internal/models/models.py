from sqlalchemy import Integer, Double
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


# Return non-private variables of models
def __publicvars__(obj=object):
    return [attr for attr in vars(obj)
              if not (attr.startswith('__') or attr.startswith('_'))]


class USERMETRICS(Base):
    __tablename__ = 'user_metrics'
    user_id = mapped_column(Integer, primary_key=True)
    total_experiments = mapped_column(Integer, nullable=False)
    average_experiments_time = mapped_column(Double, nullable=False)
    most_common_used_compound = mapped_column(Integer, nullable=True)

# add other models here e.g. class Model(Base):

