#!/usr/bin/python3
"""defining the app module for the REST API"""

from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={'/*': {'origins': "0.0.0.0"}})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.teardown_appcontext
def teardown_appcontext(exception=None):
    """close the storage session"""
    storage.close()


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST') if os.getenv('HBNB_API_HOST') else '0.0.0.0'
    port = getenv('HBNB_API_PORT') if os.getenv('HBNB_API_HOST') else '5000'
    app.run(host=host, port=port, threaded=True)
