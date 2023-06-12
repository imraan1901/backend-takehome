import os
from sqlalchemy import create_engine, URL, NullPool
from internal.models import models
import pandas

URL_OBJECT = URL.create(
    "postgresql+psycopg2",
    username=os.getenv('DB_USERNAME'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_TABLE'),
)

def init_db() -> int:
    try:
        # Connect to an existing postgres database, close after use
        engine = create_engine(URL_OBJECT, poolclass=NullPool)

        # If table is in database skip creation
        models.USERMETRICS.__table__.create(engine, checkfirst=True)
        return 0

    except Exception as error:
        print(error)
        return 1


def insert_table_into_db(data_df: pandas.DataFrame) -> int:
    try:
        # Connect to an existing postgres database, close after use
        engine = create_engine(URL_OBJECT, poolclass=NullPool)

        # Insert data into database
        data_df.to_sql(models.USERMETRICS.__tablename__, engine, if_exists='replace', index=False)
        return 0

    except Exception as error:
        print(error)
        return 1


def get_data_from_db() -> ({}, int):
    try:
        # Connect to an existing postgres database, close after use
        engine = create_engine(URL_OBJECT, poolclass=NullPool)
        connection = engine.connect()
        result = connection.execute(models.USERMETRICS.__table__.select())
        return_dict = dict()
        return_dict[models.USERMETRICS.__tablename__] = list()

        # Get the public variables in USERMETRICS
        header = models.__publicvars__(models.USERMETRICS)

        # Combine the header, the data and add it to the return_dict
        for res in result:
            return_dict[models.USERMETRICS.__tablename__].append(dict(zip(header, res)))

        return return_dict


    except Exception as error:
        print("Error while processing request", error)
        return {"message": "error while processing request"}, 400
