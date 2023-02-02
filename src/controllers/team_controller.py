from app import db_connection
from bson.json_util import ObjectId
from src.helpers.json_encoder import MongoJSONEncoder
import json
from flask import abort
from src.constants.constants import Constants


#Read Teams
def get_alll_teams():
    try:
        teams =list(db_connection.get_collection('Equipo').find())
        json_teams = json.loads(MongoJSONEncoder().encode(teams))
        if teams == [] :
            abort(404,Constants.no_team)
        else:
            return {'status': 'true', 'data': json_teams }
    except:
        abort(500, Constants.system_fail)

#Create Team
def add_team(request):
    try:
        team = request.get_json()['name']
        validate_team = list(db_connection.get_collection('Equipo').find({"name": team}))
        if validate_team != []:
            abort(400,Constants.team_exists)
        db_connection.get_collection('Equipo').insert_one({'name': team})
        return {'status': 'true', 'data': 'Team '+team+' created' }
    except:
        abort(500, Constants.system_fail)
#Update team
def refresh_team(request, id):
    new_name = request.get_json()['newName']
    team = list(db_connection.get_collection('Equipo').find({"_id": ObjectId(id)}))
    if team == [] :
        abort(404, Constants.no_team)
    else:
        db_connection.get_collection('Equipo').find_one_and_replace({'_id': ObjectId(id)}, {'name': new_name})
        return {'status': 'true', 'data': 'Updated team' }

   

#Delete team
def remove_team(id):
    try:
        team = list(db_connection.get_collection('Equipo').find({"_id": ObjectId(id)}))
        if team == [] :
            abort(404, Constants.no_team)
        else:
            db_connection.get_collection('Equipo').delete_one({'_id': ObjectId(id   )})
            return {'status': 'true', 'data': 'Team removed' }
    except:
        abort(500, Constants.system_fail)
   

#get A team
def get_team(request):
    try:
        team = request.args.get('team')
        teams = list(db_connection.get_collection('Equipo').find({"_id": ObjectId(team)}))
        if teams == []:
            abort(404, Constants.no_team)
        else:
            teams = json.loads(MongoJSONEncoder().encode(teams))
            return {'status': 'true', 'data': teams }
    except:
        abort(500, Constants.system_fail)