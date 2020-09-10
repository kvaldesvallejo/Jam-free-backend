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
from models import db, User, Teacher, Student
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

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# Create a new user 
@app.route('/user', methods=['POST'])
def create_user():
    # try:
    body = request.get_json()
    # check if this email already exists
    user = User.query.filter_by(email=body['email']).first()
    if body is None:
        raise APIException("You need to specify the request body as a json object", 400)
    # Validations
    if 'email' not in body:
        raise APIException("You need to specify an email", 400)
    # Exception when user exists
    if user is not None: 
        raise APIException("email is in use", 400)
    if 'first_name' not in body:
        raise APIException("You need to specify a first name", 400)
    if 'last_name' not in body:
        raise APIException("You need to specify a last name", 400)
    if 'password' not in body:
        raise APIException("You need to specify a password", 400)
    if 'account_type' not in body:
        raise APIException("You need to specify account type", 400)
    if 'language' not in body:
        raise APIException("You need to specify your language", 400)
    user1 = User(first_name=body['first_name'], last_name=body['last_name'], email=body['email'], password=body['password'], account_type=body['account_type'], language=body['language'])
    db.session.add(user1)
    db.session.commit()
    return jsonify("Success", 200)
    # except:
    #     return jsonify('Ohh no!! something went wrong, please try again', 400)

# Single Users
@app.route('/user/<int:user_id>', methods=['PUT', 'GET'])
def handle_single_user(user_id):
    body = request.get_json()
    target_user = User.query.get(user_id)
    # Modify an user
    if request.method == 'PUT':
        if target_user is None:
            raise APIException('User not found', 404)
        if "first_name" in body:
            target_user.first_name = body["first_name"]
        if "last_name" in body:
            target_user.last_name = body["last_name"]
        if "account_type" in body:
            target_user.account_type = body["account_type"]
        if "email" in body:
            target_user.email = body["email"]
        if "language" in body:
            target_user.language = body["language"]
        db.session.commit()
        return jsonify("Success", 200)
    # Get an user
    if request.method == 'GET':
        if target_user is None:
            raise APIException('User not found', 404)
        return jsonify(target_user.serialize(), 200)
    return jsonify("Invalid Method", 404)

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
