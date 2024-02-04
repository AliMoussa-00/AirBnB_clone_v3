#!/usr/bin/python3
"""defining the app module for the REST API"""

from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)

cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_appcontext(exception=None):
    """close the storage session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """creating a custom response for code 404"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST') if getenv('HBNB_API_HOST') else '0.0.0.0'
    port = getenv('HBNB_API_PORT') if getenv('HBNB_API_PORT') else '5000'
    app.run(host=host, port=port, threaded=True)
