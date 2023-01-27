from flask import Flask

#Import DB connection
from src.database.db import db_connection

app = Flask(__name__)

#Connect to DB
db_connection()


@app.route('/')
def home():
    return 'Hello, World!'

#Import routes
import src.routes.team_route
import src.routes.tournament_route
import src.routes.match_route