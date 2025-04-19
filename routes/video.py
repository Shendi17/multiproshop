from flask import Blueprint, request, jsonify
from app import db
from models.video import Video

video_blueprint = Blueprint('video', __name__)

# GET all videos
@video_blueprint.route('/videos', methods=['GET'])
def get_videos():
    videos = Video.query.all()
    return jsonify([v.id for v in videos])

# GET one video
@video_blueprint.route('/videos/<int:video_id>', methods=['GET'])
def get_video(video_id):
    video = Video.query.get_or_404(video_id)
    return jsonify({'id': video.id})

# CREATE a video
@video_blueprint.route('/videos', methods=['POST'])
def create_video():
    data = request.json
    video = Video(**data)
    db.session.add(video)
    db.session.commit()
    return jsonify({'id': video.id}), 201

# UPDATE a video
@video_blueprint.route('/videos/<int:video_id>', methods=['PUT'])
def update_video(video_id):
    video = Video.query.get_or_404(video_id)
    data = request.json
    for key, value in data.items():
        setattr(video, key, value)
    db.session.commit()
    return jsonify({'id': video.id})

# DELETE a video
@video_blueprint.route('/videos/<int:video_id>', methods=['DELETE'])
def delete_video(video_id):
    video = Video.query.get_or_404(video_id)
    db.session.delete(video)
    db.session.commit()
    return jsonify({'result': True})
