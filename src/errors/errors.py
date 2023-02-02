from flask import jsonify
from app import app

@app.errorhandler(404)
def resource_not_found(e):
    return {'status': 'false', 'data': {'code': 404, 'message': str.split(str(e),': ')[1]} }, 404

@app.errorhandler(400)
def bad_request(e):
    return {'status': 'false', 'data': {'code': 400, 'message': str.split(str(e),': ')[1]} }, 400

@app.errorhandler(500)
def internal_server_error(e):
    # note that we set the 500 status explicitly
     return {'status': 'false', 'data': {'code': 500, 'message':  str.split(str(e),': ')[1]} }, 500
