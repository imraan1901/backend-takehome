from sqlalchemy import create_engine, URL, NullPool
from internal.models import models
import pandas


def init_db() -> int:
    try:
        # Would be env variables on machine
        url_object = URL.create(
            "postgresql+psycopg2",
            username="postgres",
            password="postgres",
            host="db",
            database="postgres",
        )
        # Connect to an existing postgres database, close after use
        engine = create_engine(url_object, poolclass=NullPool)

        # If table is in database skip creation
        models.USERMETRICS.__table__.create(engine, checkfirst=True)
        return 0

    except Exception as error:
        print(error)
        return 1


def insert_table_into_db(data_df: pandas.DataFrame) -> int:
    try:
        # Would be env variables on machine
        url_object = URL.create(
            "postgresql+psycopg2",
            username="postgres",
            password="postgres",
            host="db",
            database="postgres",
        )
        # Connect to an existing postgres database, close after use
        engine = create_engine(url_object, poolclass=NullPool)

        # Insert data into database
        data_df.to_sql(models.USERMETRICS.__tablename__, engine, if_exists='append', index=False)
        return 0

    except Exception as error:
        print(error)
        return 1


def get_data_from_db() -> ({}, int):
    try:
        # Would be env variables on machine
        url_object = URL.create(
            "postgresql+psycopg2",
            username="postgres",
            password="postgres",
            host="db",
            database="postgres",
        )
        # Connect to an existing postgres database, close after use
        engine = create_engine(url_object, poolclass=NullPool)
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
