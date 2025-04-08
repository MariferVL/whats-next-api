from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime
from app.models import ClassSession

schedule_bp = Blueprint('schedule', __name__)

@schedule_bp.route('/schedule', methods=['GET'])
def get_schedule():
    """
    Retrieve the schedule for a given date.
    Query parameter: ?date=-DD-MM-YYYY
    """
    date_str = request.args.get('date')
    if not date_str:
        return jsonify({"error": "Date query parameter is required (DD-MM-YYYY)."}), 400
    try:
        query_date = datetime.strptime(date_str, "%d-%m-%Y").date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Use DD-MM-YYYY."}), 400

    sessions = ClassSession.query.filter_by(date=query_date).all()
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
