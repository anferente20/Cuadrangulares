from app import db_connection
from bson.json_util import ObjectId
from src.helpers.json_encoder import MongoJSONEncoder
import json
from flask import abort
from src.constants.constants import Constants
from src.database.register import update_tournament, register_match, delete_match

#Read matches
def get_all_matches():
    matches = list(db_connection.get_collection('Partido').find())
    if matches == [] :
        abort(404,Constants.no_match)
    else:
        json_matches = json.loads(MongoJSONEncoder().encode(matches))
        return {'status': 'true', 'data': json_matches }


#Create match
def add_match(request):
    request_json = request.get_json()
    try:
        tournament = request_json['tournament']
       
        #load teams
        local_team = request_json['local_team']
        visit_team = request_json['visit_team']
        
        return register_match(tournament, local_team, visit_team)
    except:
        abort(500, Constants.system_fail)

#Update match
def refresh_match(request, id):
    request_json = request.get_json()
    try:
        #get old info
        match = list(db_connection.get_collection('Partido').find({"_id": ObjectId(id)}))
        if match == [] :
            abort(404, Constants.no_match)
        else:
             #get new info
            previous_result = [match[0]['match']['local_goals'], match[0]['match']['visit_goals']]
            updated_info = {}
            updated_info = match[0]['match']
            updated_info = get_match_structure(request_json, updated_info)
            db_connection.get_collection('Partido').find_one_and_replace({'_id': ObjectId(id)}, {'tournament':match[0]['tournament'],'match': updated_info})
            tournaments = list(db_connection.get_collection('Torneo').find({"_id": ObjectId(match[0]['tournament'])}))
            tournaments = json.loads(MongoJSONEncoder().encode(tournaments))
     

            tournament_info = {
                'teams': {
                    updated_info['local_team_position']:{
                        'goals_scored': sum_results( updated_info['local_goals'], tournaments[0]['teams'][updated_info['local_team_position']]['goals_scored'], previous_result[0]),
                        'goals_recived': sum_results(updated_info['visit_goals'], tournaments[0]['teams'][updated_info['local_team_position']]['goals_recived'], previous_result[1]),
                        'points': sum_results(calcule_points(updated_info['local_goals'], updated_info['visit_goals']), tournaments[0]['teams'][updated_info['local_team_position']]['points'], calcule_points(previous_result[0], previous_result[1])  )
                    },
                    updated_info['visit_team_position']:{
                        'goals_scored': sum_results(updated_info['visit_goals'], tournaments[0]['teams'][updated_info['visit_team_position']]['goals_scored'], previous_result[1]),
                        'goals_recived': sum_results(updated_info['local_goals'], tournaments[0]['teams'][updated_info['visit_team_position']]['goals_recived'], previous_result[0]),
                        'points':  sum_results(calcule_points(updated_info['visit_goals'], updated_info['local_goals']), tournaments[0]['teams'][updated_info['visit_team_position']]['points'], calcule_points(previous_result[1], previous_result[0]))
                    }
                }
            }
            update_tournament(tournament_info, match[0]['tournament'])
            return {'status': 'true', 'data': 'Updated match' }
    except:
        abort(500, Constants.system_fail)
   

#Delete match
def remove_match(id):
    try:
        delete_match(id)
        return {'status': 'true', 'data': 'match removed' }
    except:
        abort(500, Constants.system_fail)
   

#get A match
def get_match(request):
    match = request.args.get('match')
    matches = list(db_connection.get_collection('Partido').find({"_id": ObjectId(match)}))
    if matches == []:
        abort(404, Constants.no_match)
    else:
        matches = json.loads(MongoJSONEncoder().encode(matches))
        return {'status': 'true', 'data': matches }

def get_match_structure(new_info, updated_info):
    for info in updated_info:
        if info in new_info:
            updated_info[info] = new_info[info]
    return updated_info
    

def calcule_points(goals_scored, goals_recived):
    if goals_scored > goals_recived:
        return 3
    elif goals_scored == goals_recived:
        return 1
    else:
        return 0

def sum_results(new_result, registered, old_result):
    if registered != -1:
        new_result += registered
    if old_result != -1:
        new_result -= old_result
    return new_result