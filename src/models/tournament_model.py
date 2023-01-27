from pymongo import Document
from pymongo import  StringField, NumberField

class Tournament(Document):
    name = StringField(max_length=60, required=True, unique=False)
    puntos_victoria = NumberField()
    puntos_empate = NumberField()
    puntos_derrota = NumberField()