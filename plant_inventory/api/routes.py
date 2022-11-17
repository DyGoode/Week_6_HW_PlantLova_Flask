from flask import Blueprint, request, jsonify
from plant_inventory.helpers import token_required
from plant_inventory.models import db, Plant, plant_schema, plants_schema

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return { 'some': 'value'}

@api.route('/plants', methods = ['POST'])
@token_required
def create_plant(current_user_token):
    name = request.json['name']
    species = request.json['species']
    description = request.json['description']
    typical_climate = request.json['typical_climate']
    known_uses = request.json['known_uses']
    years_grown = request.json['years_grown']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    plant = Plant(name, species, description,typical_climate, known_uses, years_grown,user_token = user_token )

    db.session.add(plant)
    db.session.commit()

    response = plant_schema.dump(plant)
    return jsonify(response)


@api.route('/plants', methods = ['GET'])
@token_required
def get_plants(current_user_token):
    owner = current_user_token.token 
    plants = Plant.query.filter_by(user_token=owner).all()
    response = plants_schema.dump(plants)
    return jsonify(response)


@api.route('/plants/<id>', methods = ['GET'])
@token_required
def get_plant(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        plant = Plant.query.get(id)
        response = plant_schema.dump(plant)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid Token Required'}), 401


@api.route('/plants/<id>', methods = ['POST', 'PUT'])
@token_required
def update_plant(current_user_token, id):
    plant = Plant.query.get(id)
    plant.name = request.json['name']
    plant.species = request.json['species']
    plant.description = request.json['description']
    plant.typical_climate = request.json['typical_climate']
    plant.known_uses = request.json['known_uses']
    plant.years_grown = request.json['years_grown']
    plant.user_token = current_user_token.token

    db.session.commit()
    response = plant_schema.dump(plant)
    return jsonify(response)



@api.route('/plants/<id>', methods = ['DELETE'])
@token_required
def delete_plant(current_user_token, id):
    plant = Plant.query.get(id)
    db.session.delete(plant)
    db.session.commit()
    response = plant_schema.dump(plant)
    return jsonify(response)