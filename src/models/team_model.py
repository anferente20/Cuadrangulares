from pymongo import Document
from pymongo import  StringField, NumberField

class Team(Document):
    name = StringField(max_length=60, required=True, unique=False)