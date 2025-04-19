from flask import Blueprint, request, jsonify
from app import db
from models.marketplace import Marketplace

marketplace_blueprint = Blueprint('marketplace', __name__)

# GET all marketplaces
@marketplace_blueprint.route('/', methods=['GET'])
def get_marketplaces():
    marketplaces = Marketplace.query.all()
    return jsonify([m.id for m in marketplaces])

# GET one marketplace
@marketplace_blueprint.route('/<int:marketplace_id>', methods=['GET'])
def get_marketplace(marketplace_id):
    marketplace = Marketplace.query.get_or_404(marketplace_id)
    return jsonify({'id': marketplace.id})

# CREATE a marketplace
@marketplace_blueprint.route('/', methods=['POST'])
def create_marketplace():
    data = request.json
    marketplace = Marketplace(**data)
    db.session.add(marketplace)
    db.session.commit()
    return jsonify({'id': marketplace.id}), 201

# UPDATE a marketplace
@marketplace_blueprint.route('/<int:marketplace_id>', methods=['PUT'])
def update_marketplace(marketplace_id):
    marketplace = Marketplace.query.get_or_404(marketplace_id)
    data = request.json
    for key, value in data.items():
        setattr(marketplace, key, value)
    db.session.commit()
    return jsonify({'id': marketplace.id})

# DELETE a marketplace
@marketplace_blueprint.route('/<int:marketplace_id>', methods=['DELETE'])
def delete_marketplace(marketplace_id):
    marketplace = Marketplace.query.get_or_404(marketplace_id)
    db.session.delete(marketplace)
    db.session.commit()
    return jsonify({'result': True})
