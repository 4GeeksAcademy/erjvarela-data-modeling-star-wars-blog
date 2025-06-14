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
from models import db, User, People, Planet, Favorite


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


@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


@app.route('/people', methods=['GET'])
def handle_get_people():
    people_data = People.query.all()
    results = [x.serialize() for x in people_data]
    return jsonify(results), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def handle_get_people_by_id(people_id):
    if not isinstance(people_id, int):
        return jsonify({"msg": "Invalid ID"}), 400
    if people_id < 1:
        return jsonify({"msg": "Invalid ID"}), 400
    people_data = People.query.get(people_id)
    if not people_data:
        return jsonify({"msg": "People not found"}), 404
    return jsonify(people_data.serialize()), 200


@app.route('/people', methods=['POST'])
def handle_create_people():
    body = request.get_json()
    if not body:
        return jsonify({"msg": "Invalid data"}), 400
    if not body.get("name"):
        return jsonify({"msg": "Name is required"}), 400
    new_people = People(
        name=body.get("name"),
        gender=body.get("gender"),
        skin_color=body.get("skin_color"),
        hair_color=body.get("hair_color"),
        height=body.get("height"),
        eye_color=body.get("eye_color"),
        mass=body.get("mass"),
        homeworld=body.get("homeworld"),
        birth_year=body.get("birth_year"),
        url=body.get("url")
    )

    db.session.add(new_people)
    db.session.commit()
    return jsonify(new_people.serialize()), 201


@app.route('/people/<int:people_id>', methods=['PUT'])
def handle_update_people(people_id):
    if not isinstance(people_id, int) or people_id < 1:
        return jsonify({"msg": "Invalid People ID"}), 400

    person = People.query.get(people_id)
    if not person:
        return jsonify({"msg": "People not found"}), 404

    body = request.get_json()
    if not body:
        return jsonify({"msg": "Request body is missing or invalid"}), 400

    person.name = body.get("name", person.name)
    person.gender = body.get("gender", person.gender)
    person.skin_color = body.get("skin_color", person.skin_color)
    person.hair_color = body.get("hair_color", person.hair_color)
    person.height = body.get("height", person.height)
    person.eye_color = body.get("eye_color", person.eye_color)
    person.mass = body.get("mass", person.mass)
    person.homeworld = body.get("homeworld", person.homeworld)
    person.birth_year = body.get("birth_year", person.birth_year)
    person.url = body.get("url", person.url)

    db.session.commit()
    return jsonify(person.serialize()), 200


@app.route('/people/<int:people_id>', methods=['DELETE'])
def handle_delete_people(people_id):
    if not isinstance(people_id, int) or people_id < 1:
        return jsonify({"msg": "Invalid People ID"}), 400

    person = People.query.get(people_id)
    if not person:
        return jsonify({"msg": "People not found"}), 404

    db.session.delete(person)
    db.session.commit()
    return jsonify({"msg": "People deleted successfully"}), 200


@app.route('/planets', methods=['GET'])
def handle_get_planets():
    planet_data = Planet.query.all()
    results = [x.serialize() for x in planet_data]
    return jsonify(results), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def handle_get_planet_by_id(planet_id):
    if not isinstance(planet_id, int):
        return jsonify({"msg": "Invalid ID"}), 400
    if planet_id < 1:
        return jsonify({"msg": "Invalid ID"}), 400
    planet_data = Planet.query.get(planet_id)
    if not planet_data:
        return jsonify({"msg": "Planet not found"}), 404
    return jsonify(planet_data.serialize()), 200


@app.route('/planets', methods=['POST'])
def handle_create_planet():
    body = request.get_json()
    if not body:
        return jsonify({"msg": "Invalid data"}), 400
    required_fields = ["name", "climate", "surface_water", "diameter", "rotation_period",
                       "terrain", "gravity", "orbital_period", "population", "url", "description"]
    for field in required_fields:
        if field not in body:
            return jsonify({"msg": f"{field.replace('_', ' ').capitalize()} is required"}), 400

    new_planet = Planet(
        name=body.get("name"),
        climate=body.get("climate"),
        surface_water=body.get("surface_water"),
        diameter=body.get("diameter"),
        rotation_period=body.get("rotation_period"),
        terrain=body.get("terrain"),
        gravity=body.get("gravity"),
        orbital_period=body.get("orbital_period"),
        population=body.get("population"),
        url=body.get("url"),
        description=body.get("description")
    )

    db.session.add(new_planet)
    db.session.commit()
    return jsonify(new_planet.serialize()), 201


@app.route('/planets/<int:planet_id>', methods=['PUT'])
def handle_update_planet(planet_id):
    if not isinstance(planet_id, int) or planet_id < 1:
        return jsonify({"msg": "Invalid Planet ID"}), 400

    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"msg": "Planet not found"}), 404

    body = request.get_json()
    if not body:
        return jsonify({"msg": "Request body is missing or invalid"}), 400

    planet.name = body.get("name", planet.name)
    planet.climate = body.get("climate", planet.climate)
    planet.surface_water = body.get("surface_water", planet.surface_water)
    planet.diameter = body.get("diameter", planet.diameter)
    planet.rotation_period = body.get(
        "rotation_period", planet.rotation_period)
    planet.terrain = body.get("terrain", planet.terrain)
    planet.gravity = body.get("gravity", planet.gravity)
    planet.orbital_period = body.get("orbital_period", planet.orbital_period)
    planet.population = body.get("population", planet.population)
    planet.url = body.get("url", planet.url)
    planet.description = body.get("description", planet.description)

    db.session.commit()
    return jsonify(planet.serialize()), 200


@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def handle_delete_planet(planet_id):
    if not isinstance(planet_id, int) or planet_id < 1:
        return jsonify({"msg": "Invalid Planet ID"}), 400

    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"msg": "Planet not found"}), 404

    db.session.delete(planet)
    db.session.commit()
    return jsonify({"msg": "Planet deleted successfully"}), 200


@app.route('/users', methods=['GET'])
def handle_get_users():
    user_data = User.query.all()
    results = [x.serialize() for x in user_data]
    return jsonify(results), 200


@app.route('/users/favorites', methods=['GET'])
def handle_get_favorites():
    # Assuming user_id is passed as a query parameter for GET, or in body if strictly required
    user_id = request.args.get("user_id")  # More RESTful for GET
    if not user_id:
        body = request.get_json(silent=True)  # Fallback to body if needed
        if body and body.get("user_id"):
            user_id = body.get("user_id")
        else:
            return jsonify({"msg": "User ID is required (as query param 'user_id' or in body)"}), 400

    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({"msg": "User ID must be an integer"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    favorites = Favorite.query.filter_by(user_id=user_id).all()
    results = [fav.serialize() for fav in favorites]
    return jsonify(results), 200


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def handle_add_favorite_people(people_id):
    body = request.get_json()
    if not body or not body.get("user_id"):
        return jsonify({"msg": "User ID is required in the body"}), 400

    user_id = body.get("user_id")
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": f"User with id {user_id} not found"}), 404

    if not isinstance(people_id, int) or people_id < 1:
        return jsonify({"msg": "Invalid People ID"}), 400

    people_data = People.query.get(people_id)
    if not people_data:
        return jsonify({"msg": f"People with id {people_id} not found"}), 404

    existing_favorite = Favorite.query.filter_by(
        user_id=user_id, people_id=people_id).first()
    if existing_favorite:
        # 409 Conflict
        return jsonify({"msg": "People already in favorites"}), 409

    new_favorite = Favorite(
        user_id=user_id,
        people_id=people_id
    )

    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.serialize()), 201


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def handle_add_favorite_planet(planet_id):
    body = request.get_json()
    if not body or not body.get("user_id"):
        return jsonify({"msg": "User ID is required in the body"}), 400

    user_id = body.get("user_id")
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": f"User with id {user_id} not found"}), 404

    if not isinstance(planet_id, int) or planet_id < 1:
        return jsonify({"msg": "Invalid Planet ID"}), 400

    planet_data = Planet.query.get(planet_id)
    if not planet_data:
        return jsonify({"msg": f"Planet with id {planet_id} not found"}), 404

    existing_favorite = Favorite.query.filter_by(
        user_id=user_id, planet_id=planet_id).first()
    if existing_favorite:
        # 409 Conflict
        return jsonify({"msg": "Planet already in favorites"}), 409

    new_favorite = Favorite(
        user_id=user_id,
        planet_id=planet_id
    )

    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.serialize()), 201


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def handle_delete_favorite_people(people_id):
    body = request.get_json()
    if not body or not body.get("user_id"):
        return jsonify({"msg": "User ID is required in the body"}), 400

    user_id = body.get("user_id")
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": f"User with id {user_id} not found"}), 404

    if not isinstance(people_id, int) or people_id < 1:
        return jsonify({"msg": "Invalid People ID"}), 400

    favorite = Favorite.query.filter_by(
        user_id=user_id, people_id=people_id).first()
    if not favorite:
        return jsonify({"msg": "Favorite people not found for this user"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite people deleted"}), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def handle_delete_favorite_planet(planet_id):
    body = request.get_json()
    if not body or not body.get("user_id"):
        return jsonify({"msg": "User ID is required in the body"}), 400

    user_id = body.get("user_id")
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": f"User with id {user_id} not found"}), 404

    if not isinstance(planet_id, int) or planet_id < 1:
        return jsonify({"msg": "Invalid Planet ID"}), 400

    favorite = Favorite.query.filter_by(
        user_id=user_id, planet_id=planet_id).first()
    if not favorite:
        return jsonify({"msg": "Favorite planet not found for this user"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite planet deleted"}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
