
import os

from flask import Flask
from flask.json import JSONEncoder
from flask_cors import CORS


from bson import json_util, ObjectId
from datetime import datetime

import configparser

from app.api.test_routes import route_test
from app.api.user import user_route
from app.api.forecast import forecast_route




config = configparser.ConfigParser()

config.read(os.path.abspath(os.path.join(".ini")))

class MongoJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, ObjectId):
            return str(obj)
        return json_util.default(obj, json_util.CANONICAL_JSON_OPTIONS)


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['MONGO_URI'] = config["TEST"]["DB_URI"]
    app.config["SECRET_KEY"] = config["KEY"]["SECRET_KEY"]

    app.json_encoder = MongoJsonEncoder
    app.register_blueprint(route_test)
    app.register_blueprint(user_route)
    app.register_blueprint(forecast_route)

    return app


