from flask import Flask
from flask_restful import Api
from internal.transport.http import handler
from internal.db import database

app = Flask(__name__)
api = Api(app)

if __name__ == "__main__":

    handler.register_handlers(api)
    database.init_db()
    app.run(debug=True, host='0.0.0.0', port=8080)
