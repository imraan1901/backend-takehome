from flask_restful import Resource
from internal.processor import processor
from internal.db import database


class Data(Resource):

    # Maybe you want to send some data to process?
    # For now, it will accept no data and process csv resource in the "data" folder
    def post(self):
        return processor.trigger_etl()

    def get(self):
        return database.get_data_from_db()

# Add other resources here

