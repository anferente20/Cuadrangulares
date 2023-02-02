from app import db_connection
from bson.json_util import ObjectId
from src.helpers.json_encoder import MongoJSONEncoder
import json
from flask import abort
from src.constants.constants import Constants


#Read tournaments
def get_all_tournaments():
    try:
        tournaments =list(db_connection.get_collection('Torneo').find())
        json_tournaments = json.loads(MongoJSONEncoder().encode(tournaments))
        if tournaments == [] :
            abort(404,Constants.no_tournament)
        else:
            return {'status': 'true', 'data': json_tournaments }
    except:
        abort(500, Constants.system_fail)
    

#Create tournament
def add_tournament(request):
    try:
        tournament = request.get_json()['name']
        validate_tournament = list(db_connection.get_collection('Torneo').find({"name": tournament}))
        if validate_tournament != []:
            abort(400,Constants.tournament_exists)
        #load teams
        teams = request.get_json()['teams']

        #build team structure
        for team in teams:
            teams[team] = {
                'team': teams[team],
                'goals_scored': 0,
                'points': 0,
                'goals_recived': 0
            }
        db_connection.get_collection('Torneo').insert_one({'name': tournament, 'teams':teams})
        return {'status': 'true', 'data': 'tournament '+tournament+' created' }
    except:
        abort(500, Constants.system_fail)

#Update tournament
def refresh_tournament(request, id):
    request_json = request.get_json()
    try:
        #get old info
        tournament = list(db_connection.get_collection('Torneo').find({"_id": ObjectId(id)}))
        if tournament == [] :
            abort(404, Constants.no_tournament)
        else:
             #get new info
            new_name = ''
            if 'newName' in request_json:
                new_name = request_json['newName']

            updated_teams = {}
            if 'teams' in request_json:
                new_teams = request_json['teams']
                updated_teams = tournament[0]['teams']
                updated_teams = get_teams_structure(new_teams, updated_teams)

            updated_info = get_update_structure(new_name, updated_teams)
            db_connection.get_collection('Torneo').find_one_and_replace({'_id': ObjectId(id)}, updated_info)
            return {'status': 'true', 'data': 'Updated tournament' }
    except:
        abort(500, Constants.system_fail)
   

#Delete tournament
def remove_tournament(id):
    try:
        tournament = list(db_connection.get_collection('Torneo').find({"_id": ObjectId(id)}))
        if tournament == [] :
            abort(404, Constants.no_tournament)
        else:
            db_connection.get_collection('Torneo').delete_one({'_id': ObjectId(id   )})
            return {'status': 'true', 'data': 'tournament removed' }
    except:
        abort(500, Constants.system_fail)
   

#get A tournament
def get_tournament(request):
    try:
        tournament = request.args.get('tournament')
        tournaments = list(db_connection.get_collection('Torneo').find({"_id": ObjectId(tournament)}))
        if tournaments == []:
            abort(404, Constants.no_tournament)
        else:
            tournaments = json.loads(MongoJSONEncoder().encode(tournaments))
            return {'status': 'true', 'data': tournaments }
    except:
        abort(500, Constants.system_fail)

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
    print(stucture)
    return stucture