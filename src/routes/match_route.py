from app import app
from flask import request
from src.controllers.match_controller import get_all_matches, get_match, refresh_match, remove_match, add_match

path = '/matches/'

@app.route(path+'add', methods=['POST'])
def create_match():
    return add_match(request)

@app.route(path, methods=['GET'])
def get_matches():
    return get_all_matches()


@app.route(path+'update/<path:id>', methods=['PUT'])
def update_match(id):
    return refresh_match(request, id)

@app.route(path+'delete/<path:id>', methods=['DELETE'])
def delete_match(id):
    return remove_match(id)


@app.route(path+'get', methods=['GET'])
def obtain_macth():
    return get_match(request)