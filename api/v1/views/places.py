#!/usr/bin/python3
"""Defining the places module to request the places objs"""

from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage, storage_t
from models.city import City
from models.place import Place
from models.state import State
from models.user import User


@app_views.route(
        '/cities/<city_id>/places', methods=['GET'],
        strict_slashes=False)
def get_places(city_id):
    """get all places objects"""
    city = storage.all(City).get("City.{}".format(city_id))
    if not city:
        abort(404)

    objs = []
    for obj in city.places:
        objs.append(obj.to_dict())

    return jsonify(objs)


@app_views.route(
        '/places/<place_id>', methods=['GET'],
        strict_slashes=False)
def get_place(place_id):
    """get a place object by id"""
    place = storage.all(Place).get("Place.{}".format(place_id))
    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route(
        '/places/<place_id>', methods=['DELETE'],
        strict_slashes=False)
def delete_place(place_id):
    """delete a place object by id"""
    place = storage.all(Place).get("Place.{}".format(place_id))
    if not place:
        abort(404)

    place.delete()
    storage.save()
    return jsonify({})


@app_views.route(
        '/cities/<city_id>/places', methods=['POST'],
        strict_slashes=False)
def create_place(city_id):
    """create a new place object"""
    city = storage.all(City).get("City.{}".format(city_id))
    if not city:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({'error': 'Missing user_id'}), 400)

    user_id = request.get_json()['user_id']
    user = storage.all(User).get("User.{}".format(user_id))
    if not user:
        abort(404)

    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)

    name = request.get_json()['name']
    place = Place(city_id=city_id, user_id=user_id, name=name)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route(
        '/places/<place_id>', methods=['PUT'],
        strict_slashes=False)
def update_place(place_id):
    """update place object"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    place = storage.all(Place).get("Place.{}".format(place_id))
    if not place:
        abort(404)

    ignor = ["id", "created_at", "updated_at", "user_id", "city_id"]
    for k, v in request.get_json().items():
        if k in ignor:
            continue
        setattr(place, k, v)

    place.save()
    return jsonify(place.to_dict())


@app_views.route(
        '/places_search', methods=['POST'],
        strict_slashes=False)
def search_places():
    """ search places """
    json_data = request.get_json()
    if not json_data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    states_ids = json_data.get("states")
    cities_ids = json_data.get("cities")
    amenities_ids = json_data.get('amenities')
    list_places = []

    if not states_ids and not cities_ids:
        list_places = storage.all('Place').values()

    if states_ids:
        for state_id in states_ids:
            state = storage.all(State).get("State.{}".format(state_id))
            if state:
                for city in state.cities:
                    list_places.extend(city.places)

    if cities_ids:
        for city_id in cities_ids:
            city = storage.all(City).get(f"City.{}".format(city_id))
            if city:
                list_places.extend(city.places)

    objs = []
    for place in list_places:
        objs.append(place.to_dict())
        if models.storage_t == "db":
            place_amenity = [ame.id for ame in place.amenities]
        else:
            place_amenity = place.amenity_ids

        for amenity_id in amenities_ids:
            if amenity_id not in place_amenity:
                objs.pop()
                break

    return jsonify(objs)
