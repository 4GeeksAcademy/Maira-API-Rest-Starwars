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
from models import db, User, Characters, Planets, Starships, FavCharacters, FavPlanets, FavStarships
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
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
    users = User.query.all()  # SELECT * FROM 'user';
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

@app.route('/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    user = User.query.get(user_id)
    print(user)
    user1 = user.serialize()
    return jsonify(user1), 200

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

    # Lista de registros en la tabla FavCharacters
    favorite_records_char = user.favorites_char
    print(favorite_records_char)
    favorite_char_serialized = []
    for record in favorite_records_char:
        new_favorite = record.people.serialize()
        favorite_char_serialized.append(new_favorite)

    favorite_records_plan = user.favorites_plan
    print(favorite_records_plan)
    favorite_plan_serialized = []
    for record in favorite_records_plan:
        new_favorite = record.astros.serialize()
        favorite_plan_serialized.append(new_favorite)

    favorite_records_star = user.favorites_star
    print(favorite_records_star)
    favorite_star_serialized = []
    for record in favorite_records_star:
        new_favorite = record.naves.serialize()
        favorite_star_serialized.append(new_favorite)

    return jsonify({'msg': 'Todo salió bien', 'favorite_character': favorite_char_serialized, \
                    'favorite_planets': favorite_plan_serialized, \
                    'favorite_starships': favorite_star_serialized}), 200

@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Characters.query.all()
    characters_serialized = []
    for character in characters:
        characters_serialized.append(character.serialize())
    response_body = {
        'characters': characters_serialized
    }
    return jsonify(response_body), 200

@app.route('/character/<int:character_id>', methods=['GET'])
def get_one_character(character_id):
    character = Characters.query.get(character_id)
    print(character)
    character1 = character.serialize()
    return jsonify(character1), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    planets_serialized = []
    for planet in planets:
        planets_serialized.append(planet.serialize())
    response_body = {
        'planets': planets_serialized
    }
    return jsonify(response_body), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    planet = Planets.query.get(planet_id)
    print(planet)
    planet1 = planet.serialize()
    return jsonify(planet1), 200

@app.route('/starships', methods=['GET'])
def get_starships():
    starships = Starships.query.all()
    starships_serialized = []
    for starship in starships:
        starships_serialized.append(starship.serialize())
    response_body = {
        'starships': starships_serialized
    }
    return jsonify(response_body), 200

@app.route('/starship/<int:starship_id>', methods=['GET'])
def get_one_starship(starship_id):
    starship = Starships.query.get(starship_id)
    print(starship)
    starship1 = starship.serialize()
    return jsonify(starship1), 200

@app.route('/favorite/<int:user_id>/character/<int:character_id>', methods=['POST'])
def add_favorite_character(user_id, character_id):
    body = request.get_json(silent=True)
    print(body)
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': 'El usuario no existe'}), 404
    character = Characters.query.get(character_id)
    if character is None:
        return jsonify({'msg': 'El personaje no existe'}), 404
    new_character_favorite = FavCharacters(user_id=user_id, character_id=character_id)
    if new_character_favorite:
        return jsonify({'msg': 'El personaje ya está en favoritos'}), 400
    
    db.session.add(new_character_favorite)
    db.session.commit()
    return jsonify({'msg': 'Nuevo favorito agregado'}), 200

@app.route('/favorite/<int:user_id>/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id, planet_id):
    body = request.get_json(silent=True)
    print(body)
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': 'El usuario no existe'}), 404
    planet = Planets.query.get(planet_id)
    if planet is None:
        return jsonify({'msg': 'El planeta no existe'}), 404
    new_planet_favorite = FavPlanets(user_id=user_id, planet_id=planet_id)
    if new_planet_favorite:
        return jsonify({'msg': 'El planeta ya está en favoritos'}), 400
    
    db.session.add(new_planet_favorite)
    db.session.commit()
    return jsonify({'msg': 'Nuevo favorito agregado'}), 200

@app.route('/favorite/<int:user_id>/starship/<int:starship_id>', methods=['POST'])
def add_favorite_starship(user_id, starship_id):
    body = request.get_json(silent=True)
    print(body)
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': 'El usuario no existe'}), 404
    starship = Starships.query.get(starship_id)
    if starship is None:
        return jsonify({'msg': 'La nave no existe'}), 404
    new_starship_favorite = FavStarships(user_id=user_id, starship_id=starship_id)
    if new_starship_favorite:
        return jsonify({'msg': 'Esta ya está en favoritos'}), 400
    
    db.session.add(new_starship_favorite)
    db.session.commit()
    return jsonify({'msg': 'Nuevo favorito agregado'}), 200

@app.route('/favorite/<int:user_id>/character/<int:character_id>', methods=['DELETE'])
def remove_favorite_character(user_id, character_id):
    favorite = FavCharacters.query.filter_by(user_id=user_id, character_id=character_id).first()
    if favorite is None:
        return jsonify({'msg': 'Favorito no encontrado'}), 404    
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({'msg': 'Favorito eliminado!'}), 200

@app.route('/favorite/<int:user_id>/planet/<int:planet_id>', methods=['DELETE'])
def remove_favorite_planet(user_id, planet_id):
    favorite = FavPlanets.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if favorite is None:
        return jsonify({'msg': 'Favorito no encontrado'}), 404    
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({'msg': 'Favorito eliminado!'}), 200

@app.route('/favorite/<int:user_id>/starship/<int:starship_id>', methods=['DELETE'])
def remove_favorite_starship(user_id, starship_id):
    favorite = FavStarships.query.filter_by(user_id=user_id, starship_id=starship_id).first()
    if favorite is None:
        return jsonify({'msg': 'Favorito no encontrado'}), 404    
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({'msg': 'Favorito eliminado!'}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
