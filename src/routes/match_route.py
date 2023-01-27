from app import app

path = '/matches/'

@app.route(path+'add', methods=['POST'])
def create_match():
    return 'Create matches!'

@app.route(path, methods=['GET'])
def get_matches():
    return 'Get matches!'


@app.route(path+'update', methods=['PUT'])
def update_match():
    return 'Update matches!'

@app.route(path+'delete', methods=['DELETE'])
def delete_match():
    return 'GET matches!'