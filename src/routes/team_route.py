from app import app
from src.controllers.team_controller import get_alll_teams, add_team, refresh_team, remove_team, get_team
from flask import request

path = '/teams/'

@app.route(path+'add', methods=['POST'])
def create_team():
    return add_team(request)

@app.route(path, methods=['GET'])
def get_teams():
    return get_alll_teams()


@app.route(path+'update/<path:id>', methods=['PUT'])
def update_team(id):
    return refresh_team(request, id)

@app.route(path+'delete/<path:id>', methods=['DELETE'])
def delete_team(id):
    return remove_team(id)

@app.route(path+'get', methods=['GET'])
def obtain_team():
    return get_team(request)