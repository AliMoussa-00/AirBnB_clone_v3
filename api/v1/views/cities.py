#!/usr/bin/python3
"""Defining the cities module to request the cities objs"""

from flask import abort, jsonify, request

from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities(state_id):
    """get cities  """
    objs = []
    state = storage.all(State).get(f"State.{state_id}")

    if not state:
        abort(404)

    for city in state.cities:
        objs.append(city.to_dict())

    return jsonify(objs)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city_by_id(city_id):
    """get City by id """
    city = storage.all(City).get(f"City.{city_id}")
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city_by_id(city_id):
    """delete City by id """
    city = storage.all(City).get(f"City.{city_id}")
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """create City """

    state = storage.all(State).get(f"State.{state_id}")
    if not state:
        abort(404)

    json_data = request.get_json()

    if type(json_data) is not dict:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in json_data:
        return jsonify({'error': 'Missing name'}), 400

    new_city = City(state_id=state_id, name=json_data.get('name'))
    new_city.save()
    return (new_city.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """ update City object"""
    city = storage.all(City).get(f"City.{city_id}")
    if not city:
        abort(404)

    json_data = request.get_json()
    if type(json_data) is not dict:
        return jsonify({'error': 'Not a JSON'}), 400

    ignore = ["id", "state_id", "created_at", "updated_at"]
    for k, v in json_data.items():
        if k not in ignore:
            setattr(city, k, v)

    city.save()
    return jsonify(city.to_dict()), 200
