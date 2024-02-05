#!/usr/bin/python3
"""Defining the places reviews module to request the reviews objs"""

from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route(
        '/places/<place_id>/reviews', methods=['GET'],
        strict_slashes=False)
def get_all_review(place_id):
    """all revies objects"""
    objs = []
    place = storage.all(Place).get("Place.{}".format(place_id))
    if not place:
        abort(404)
    for review in place.reviews:
        objs.append(review.to_dict())

    return jsonify(objs)


@app_views.route(
        '/reviews/<review_id>', methods=['GET'],
        strict_slashes=False)
def get_review_by_id(review_id):
    """get review by id"""
    review = storage.all(Review).get("Review.{}".format(review_id))
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route(
        '/reviews/<review_id>', methods=['DELETE'],
        strict_slashes=False)
def delete_review_by_id(review_id):
    """delete review by id"""
    review = storage.all(Review).get("Review.{}".format(review_id))
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/places/<place_id>/reviews', methods=['POST'],
        strict_slashes=False)
def create_review(place_id):
    """create review"""
    place = storage.all(Place).get("Place.{}".format(place_id))
    if place is None:
        abort(404)

    json_data = request.get_json()
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in json_data:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)

    user_id = json_data.get('user_id')
    user = storage.all(User).get("User.{}".format(user_id))
    if user is None:
        abort(404)
    if 'text' not in json_data:
        return make_response(jsonify({'error': 'Missing text'}), 400)

    new_review = Review(place_id=place_id, **json_data)
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route(
        '/reviews/<review_id>', methods=['PUT'],
        strict_slashes=False)
def update_review(review_id):
    """update review object"""
    json_data = request.get_json()
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    review = storage.all(Review).get("Review.{}".format(review_id))
    if review is None:
        abort(404)

    ignore = ["id", "user_id", "place_id", "created_at", "updated_at"]
    for k, v in json_data.items():
        if k not in ignore:
            setattr(review, k, v)

    review.save()
    return jsonify(review.to_dict()), 200
