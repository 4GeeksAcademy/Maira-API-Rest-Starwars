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

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
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

@app.route('/users', methods=['GET'])
def handle_hello():
    users = User.query.all() #SELECT * FROM 'user';
    # print(users) # [disns@4geek.com, dia@noche.com]
    users_serialized = []
    for user in users:
        users_serialized.append(user.serialize())
    # print(type(users[0])) # <class 'models.User'> <-- esto no se puede convertir a JSON porque no es un diccionario, es una clase
    # user1 = users[0].serialize()
    # print(user1) # <-- esto sí es un diccionario y se puede convertir a JSON
    response_body = {
        'msg': 'Hello, this is your GET /user response ',
        'users': users_serialized
    }
    return jsonify(response_body), 200

@app.route('/user', methods=['POST'])
def add_user():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Debes enviar información en el body'}), 400
    if 'email' not in body:
        return jsonify({'msg': 'El campo "email" es obligatorio'}), 400
    if 'password' not in body:
        return jsonify({'msg': 'El campo "password" es obligatorio'}), 400
    print(body)
    new_user = User()
    new_user.email = body['email']
    new_user.password = body['password']
    new_user.is_active = True
    print(new_user)
    print(type(new_user))
    
    db.session.add(new_user)  # esto agrega la nueva info
    db.session.commit()  # y esto es para guardar la nueva info en la db
    return jsonify({'msg': 'Nuevo usuario registrado', 'user': new_user.serialize()}), 200

@app.route('/user_favorites/<int:user_id>', methods=['GET'])
def get_favorites(user_id):
    user = User.query.get(user_id)
    print(user)
    if user is None:
        return jsonify({'msg': f'El usuario con id {user_id} no existe.'}), 404
    favorite_records_char = user.favorites_char # Lista de registros en la tabla FavCharacters
    favorite_records_plan = user.favorites_plan
    favorite_records_star = user.favorites_star
    print(favorite_records_char)
    #print(favorite_records_char[0].people.serialize())
    print(favorite_records_char[0].people.serialize())

    favorite_char_serialized = []

    for record in favorite_records_char:
        new_favorite = record.people.serialize()
        favorite_char_serialized.append(new_favorite)

    return jsonify({'msg': 'Todo salió bien', 'favorite_character': favorite_char_serialized}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
