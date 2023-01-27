from app import app

path = '/tournaments/'

@app.route(path+'add', methods=['POST'])
def create_tournament():
    return 'Create tournaments!'

@app.route(path, methods=['GET'])
def get_tournaments():
    return 'Get tournaments!'


@app.route(path+'update', methods=['PUT'])
def update_tournament():
    return 'Update tournaments!'

@app.route(path+'delete', methods=['DELETE'])
def delete_tournament():
    return 'GET tournaments!'