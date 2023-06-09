from sqlalchemy import Integer, Double, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


# Return non-private variables of models in order
def __publicvars__(obj=object) -> [str]:
    return [attr for attr in vars(obj) if not (attr.startswith('__') or attr.startswith('_'))]


class USERMETRICS(Base):
    __tablename__ = 'user_metrics'
    name = mapped_column(String, primary_key=True)
    total_experiments = mapped_column(Integer, nullable=True)
    average_experiments_time = mapped_column(Double, nullable=True)
    most_common_used_compound = mapped_column(String, nullable=True)

# add other models here e.g. class Model(Base):

