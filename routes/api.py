from flask import Blueprint, request, jsonify
from app import db
from models.api_integration import ApiIntegration

api_blueprint = Blueprint('api', __name__)

# GET all integrations
@api_blueprint.route('/integrations', methods=['GET'])
def get_integrations():
    integrations = ApiIntegration.query.all()
    return jsonify([a.id for a in integrations])

# GET one integration
@api_blueprint.route('/integrations/<int:api_id>', methods=['GET'])
def get_integration(api_id):
    api = ApiIntegration.query.get_or_404(api_id)
    return jsonify({'id': api.id})

# CREATE an integration
@api_blueprint.route('/integrations', methods=['POST'])
def create_integration():
    data = request.json
    api = ApiIntegration(**data)
    db.session.add(api)
    db.session.commit()
    return jsonify({'id': api.id}), 201

# UPDATE an integration
@api_blueprint.route('/integrations/<int:api_id>', methods=['PUT'])
def update_integration(api_id):
    api = ApiIntegration.query.get_or_404(api_id)
    data = request.json
    for key, value in data.items():
        setattr(api, key, value)
    db.session.commit()
    return jsonify({'id': api.id})

# DELETE an integration
@api_blueprint.route('/integrations/<int:api_id>', methods=['DELETE'])
def delete_integration(api_id):
    api = ApiIntegration.query.get_or_404(api_id)
    db.session.delete(api)
    db.session.commit()
    return jsonify({'result': True})
