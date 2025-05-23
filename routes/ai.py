from flask import Blueprint, request, jsonify
from extensions import db
from models.ai_recommendation import AIRecommendation

ai_blueprint = Blueprint('ai', __name__)

# GET all recommendations
@ai_blueprint.route('/ai/recommendations', methods=['GET'])
def get_recommendations():
    recs = AIRecommendation.query.all()
    return jsonify([r.id for r in recs])

# GET one recommendation
@ai_blueprint.route('/ai/recommendations/<int:rec_id>', methods=['GET'])
def get_recommendation(rec_id):
    rec = AIRecommendation.query.get_or_404(rec_id)
    return jsonify({'id': rec.id})

# CREATE a recommendation
@ai_blueprint.route('/ai/recommendations', methods=['POST'])
def create_recommendation():
    data = request.json
    rec = AIRecommendation(**data)
    db.session.add(rec)
    db.session.commit()
    return jsonify({'id': rec.id}), 201

# UPDATE a recommendation
@ai_blueprint.route('/ai/recommendations/<int:rec_id>', methods=['PUT'])
def update_recommendation(rec_id):
    rec = AIRecommendation.query.get_or_404(rec_id)
    data = request.json
    for key, value in data.items():
        setattr(rec, key, value)
    db.session.commit()
    return jsonify({'id': rec.id})

# DELETE a recommendation
@ai_blueprint.route('/ai/recommendations/<int:rec_id>', methods=['DELETE'])
def delete_recommendation(rec_id):
    rec = AIRecommendation.query.get_or_404(rec_id)
    db.session.delete(rec)
    db.session.commit()
    return jsonify({'result': True})
