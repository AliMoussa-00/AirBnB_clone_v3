#!/usr/bin/python3
"""Defining the users module to request the users objs"""

from flask import abort, jsonify, request

from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def get_all_users():
    """all Users objects """
    objs = []
    all_users = storage.all(User).values()

    for obj in all_users:
        objs.append(obj.to_dict())

    return jsonify(objs)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """get user by id """
    user = storage.all(User).get(f"User.{user_id}")
    if user:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    """delete user by id """
    user = storage.all(User).get(f"User.{user_id}")
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'])
def create_user():
    """ create user """
    json_data = request.get_json()
    if type(json_data) is not dict:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'email' not in json_data:
        return jsonify({'error': 'Missing email'}), 400
    if 'password' not in json_data:
        return jsonify({'error': 'Missing password'}), 400

    email = json_data.get('email')
    password = json_data.get('password')
    new_user = User(email=email, password=password)
    new_user.save()
    return (new_user.to_dict()), 200


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """update user object"""
    json_data = request.get_json()
    if type(json_data) is not dict:
        return jsonify({'error': 'Not a JSON'}), 400

    user = storage.all(User).get(f"User.{user_id}")
    if not user:
        abort(404)

    ignore = ["id", "email", "created_at", "updated_at"]
    for k, v in json_data.items():
        if k not in ignore:
            setattr(user, k, v)

    user.save()
    return jsonify(user.to_dict()), 200
