from models.team_model import Team
from models.tournament_model import Tournament
from pymongo import Document
from pymongo import  NumberField, ReferenceField


class Match(Document):
    tournament = ReferenceField(Tournament, required=True)
    local_team = ReferenceField(Team, required=True)
    visit_team = ReferenceField(Team, required=True)
    local_goals = NumberField()
    visit_goals = NumberField()