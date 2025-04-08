from flask import Blueprint, request, abort, jsonify
from flask_jwt_extended import jwt_required 
from datetime import datetime
from app.models import ClassSession
from app.extensions import db
from app.controllers.class_controller import create_class_session, update_class_session, delete_class_session
from app.utils.response_formatter import success_response, error_response

classes_bp = Blueprint('classes', __name__)

@classes_bp.route('/classes', methods=['GET'])
def get_classes():
    """Retrieve all class sessions."""
    sessions = ClassSession.query.all()
    sessions_list = [{
        "id": s.id,
        "title": s.title,
        "description": s.description,
        "date": s.date.strftime("%d-%m-%Y"),
        "start_time": s.start_time.strftime("%H:%M"),
        "end_time": s.end_time.strftime("%H:%M"),
        "professor_id": s.professor_id,
        "session_type": s.session_type
    } for s in sessions]
    return jsonify(sessions_list), 200

@classes_bp.route('/classes/<int:id>', methods=['GET'])
def get_class(id):
    """Retrieve a specific class session by ID."""
    session = db.session.get(ClassSession, id)
    if session is None:
        abort(404, description="Class session not found.")
    session_data = {
        "id": session.id,
        "title": session.title,
        "description": session.description,
        "date": session.date.strftime("%d-%m-%Y"),
        "start_time": session.start_time.strftime("%H:%M"),
        "end_time": session.end_time.strftime("%H:%M"),
        "professor_id": session.professor_id,
        "session_type": session.session_type
    }
    return jsonify(session_data), 200

@classes_bp.route('/classes', methods=['POST'])
@jwt_required()
def create_class():
    """Create a new class session."""
    data = request.get_json()
    required_fields = ["title", "date", "start_time", "end_time", "professor_id", "session_type"]
    for field in required_fields:
        if field not in data:
            return error_response(f"Missing required field: {field}", 400)
    
    return create_class_session(data)

@classes_bp.route('/classes/<int:id>', methods=['PUT'])
@jwt_required()
def update_class(id):
    """Update an existing class session."""
    data = request.get_json()
    return update_class_session(id, data)

@classes_bp.route('/classes/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_class(id):
    """Delete a class session."""
    return delete_class_session(id)
