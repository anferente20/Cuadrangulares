from app import app

path = '/teams/'

@app.route(path+'add', methods=['POST'])
def create_team():
    return 'Create Teams!'

@app.route(path, methods=['GET'])
def get_teams():
    return 'Get Teams!'


@app.route(path+'update', methods=['PUT'])
def update_team():
    return 'Update Teams!'

@app.route(path+'delete', methods=['DELETE'])
def delete_team():
    return 'GET Teams!'