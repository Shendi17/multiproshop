from flask import Blueprint, request, jsonify
from extensions import db
from models.supplier import Supplier

supplier_blueprint = Blueprint('supplier', __name__)

# GET all suppliers
@supplier_blueprint.route('/', methods=['GET'])
def get_suppliers():
    suppliers = Supplier.query.all()
    return jsonify([s.id for s in suppliers])

# GET one supplier
@supplier_blueprint.route('/<int:supplier_id>', methods=['GET'])
def get_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    return jsonify({'id': supplier.id})

# CREATE a supplier
@supplier_blueprint.route('/', methods=['POST'])
def create_supplier():
    data = request.json
    supplier = Supplier(**data)
    db.session.add(supplier)
    db.session.commit()
    return jsonify({'id': supplier.id}), 201

# UPDATE a supplier
@supplier_blueprint.route('/<int:supplier_id>', methods=['PUT'])
def update_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    data = request.json
    for key, value in data.items():
        setattr(supplier, key, value)
    db.session.commit()
    return jsonify({'id': supplier.id})

# DELETE a supplier
@supplier_blueprint.route('/<int:supplier_id>', methods=['DELETE'])
def delete_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    db.session.delete(supplier)
    db.session.commit()
    return jsonify({'result': True})
