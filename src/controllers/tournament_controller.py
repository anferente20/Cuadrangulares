from app import db_connection
from bson.json_util import ObjectId
from src.helpers.json_encoder import MongoJSONEncoder
import json
from flask import abort
from src.constants.constants import Constants
import itertools
from src.database.register import update_tournament, register_match, delete_match


#Read tournaments
def get_all_tournaments():
    tournaments =list(db_connection.get_collection('Torneo').find())
    if tournaments == [] :
        abort(404,Constants.no_tournament)
    else:
        json_tournaments = json.loads(MongoJSONEncoder().encode(tournaments))
        return {'status': 'true', 'data': json_tournaments }

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
        tournament_added = db_connection.get_collection('Torneo').insert_one({'name': tournament, 'teams':teams})
        generate_matches(teams, tournament_added.inserted_id)
        return {'status': 'true', 'data': 'tournament '+tournament+' created' }
    except:
        abort(500, Constants.system_fail)

#Update tournament
def refresh_tournament(request, id):
    request_json = request.get_json()
    try:
            update_tournament(request_json, id)
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
            matches =  matches = list(db_connection.get_collection('Partido').find({'tournament': ObjectId(id)}))
            for match in matches:
                delete_match(match['_id'])
            db_connection.get_collection('Torneo').delete_one({'_id': ObjectId(id)})
            return {'status': 'true', 'data': 'tournament removed' }
    except:
        abort(500, Constants.system_fail)
   

#get A tournament
def get_tournament(request):
    tournament = request.args.get('tournament')
    tournaments = list(db_connection.get_collection('Torneo').find({"_id": ObjectId(tournament)}))
    if tournaments == []:
        abort(404, Constants.no_tournament)
    else:
        tournaments = json.loads(MongoJSONEncoder().encode(tournaments))
        return {'status': 'true', 'data': tournaments }




def generate_matches(teams, id):
    matches = []
    combine = itertools.combinations(teams, 2)
    for c in combine:
        matches.append(c)

    for match in matches:
        register_match(id, [match[0],teams[match[0]]['team']], [match[1],teams[match[1]]['team']])

