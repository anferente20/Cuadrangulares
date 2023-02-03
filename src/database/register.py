from flask import abort
from bson.json_util import ObjectId
from src.constants.constants import Constants
from app import db_connection


def update_tournament(new_info, id):
    tournament = list(db_connection.get_collection('Torneo').find({"_id": ObjectId(id)}))
    if tournament == [] :
        abort(404, Constants.no_tournament)
    else:
            #get new info
        new_name = ''
        if 'newName' in new_info:
            new_name = new_info['newName']

        updated_teams = {}
        if 'teams' in new_info:
            new_teams = new_info['teams']
            updated_teams = tournament[0]['teams']
            updated_teams = get_teams_structure(new_teams, updated_teams)

        updated_info = get_update_structure(new_name, updated_teams)
        db_connection.get_collection('Torneo').find_one_and_replace({'_id': ObjectId(id)}, updated_info)


def get_teams_structure(new_teams, updated_teams):
    for team in updated_teams:
        if team in new_teams:
            for topic in updated_teams[team]:
                if topic in new_teams[team]:
                    updated_teams[team][topic] = new_teams[team][topic]
    return updated_teams


def get_update_structure(name, teams):
    stucture = {}
    if name != '':
        stucture['name'] = name
    
    if teams != {}:
        stucture['teams'] = teams
    return stucture


def register_match(tournament, local_team, visit_team):
    if list(db_connection.get_collection('Torneo').find({"_id": ObjectId(tournament)})) == []:
            abort(400, Constants.tournament_invalid)
    #load teams
    if list(db_connection.get_collection('Equipo').find({"_id": ObjectId(local_team[1])})) == []:
            abort(400, Constants.local_team_invalid)
    if list(db_connection.get_collection('Equipo').find({"_id": ObjectId(visit_team[1])})) == []:
            abort(400, Constants.visit_team_invalid) 

    #build dict
    info = {
            'local_team': local_team[1],
            'local_goals': -1,
            'visit_team': visit_team[1],
            'visit_goals': -1,
            'local_team_position': local_team[0],
            'visit_team_position': visit_team[0] 
            }
    db_connection.get_collection('Partido').insert_one({'tournament': tournament,'match':info})
    return {'status': 'true', 'data': 'match created' }

def delete_match(id):
    match = list(db_connection.get_collection('Partido').find({"_id": ObjectId(id)}))
    if match == [] :
        abort(404, Constants.no_match)
    else:
        db_connection.get_collection('Partido').delete_one({'_id': ObjectId(id   )})
                