#!/usr/bin/python3
"""defining the app module for the REST API"""

from os import getenv
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

APP = Flask(__name__)
APP.register_blueprint(app_views)

CORS = CORS(APP, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})


@APP.teardown_appcontext
def teardown_appcontext():
    """close the storage session"""
    storage.close()


@APP.errorhandler(404)
def not_found():
    """creating a custom response for code 404"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    HOST = getenv('HBNB_API_HOST') if getenv('HBNB_API_HOST') else '0.0.0.0'
    PORT = getenv('HBNB_API_PORT') if getenv('HBNB_API_PORT') else '5000'
    APP.run(host=HOST, port=PORT, threaded=True)
