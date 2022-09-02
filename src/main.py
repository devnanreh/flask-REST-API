"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# @app.route('/user', methods=['GET'])
# def get_users():
#     user_list = User.query.all()
#     user_list = list(map(lambda user: user.serialize(), user_list))
#     A query to the database. It is asking the database to give us all the users.
#     queryset = User.query.all()
#     user_list = [user.serialize() for user in queryset]
#     return jsonify(user_list), 200

@app.route('/users', methods=['GET'])
def get_users():
    queryset = User.query.all()
    user_list = [user.serialize() for user in queryset]
    
    return jsonify(user_list), 200

@app.route('/users/favorites', methods=['GET'])
def get_user_favorite():
    return jsonify("FAVORITOS"), 200


# It takes a GET request, and returns a JSON object containing the string 'people'
@app.route('/people', methods=['GET'])
def get_people():
    return jsonify('Aca people')

@app.route('/people/<int:people_id>', methods=['GET'])
def get_single_people(people_id):
    response_body = {"id de single": people_id}
    return jsonify(response_body)

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def post_favorite_people(people_id):
    return jsonify(people_id)

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    return jsonify(people_id)



# It takes a GET request, and returns a JSON object containing the string 'planets'
@app.route('/planets', methods=['GET'])
def get_planets():
    return jsonify('planets')

# It takes a planet_id as an argument, and returns a JSON object with the planet_id
    # :param planet_id: The id of the planet we want to get
    # :return: The planet_id
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    return jsonify(planet_id)

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def post_favorite_planet(planet_id):
    return jsonify(planet_id)

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    return jsonify(planet_id), 200



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


