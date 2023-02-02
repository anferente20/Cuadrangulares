from app import app
from flask import request
from src.controllers.tournament_controller import get_all_tournaments, get_tournament, add_tournament, refresh_tournament, remove_tournament
path = '/tournaments/'

@app.route(path+'add', methods=['POST'])
def create_tournament():
    return add_tournament(request)

@app.route(path, methods=['GET'])
def get_tournaments():
    return get_all_tournaments()


@app.route(path+'update/<path:id>', methods=['PUT'])
def update_tournament(id):
    return refresh_tournament(request, id)

@app.route(path+'delete/<path:id>', methods=['DELETE'])
def delete_tournament(id):
    return remove_tournament(id)

@app.route(path+'get', methods=['GET'])
def obtain_tournament():
    return get_tournament(request)