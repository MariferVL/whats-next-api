from flask import abort, jsonify
from datetime import datetime
from app.extensions import db
from app.models import ClassSession
from app.utils.validators import is_valid_session_schedule
from app.utils.response_formatter import success_response, error_response

def create_class_session(data):
    """
    Create a new class session after validating schedule constraints.
    """
    valid, message = is_valid_session_schedule(
        data["session_type"],
        data["date"],
        data["start_time"],
        data["end_time"]
    )
    if not valid:
        return error_response(message, 400)
    
    try:
        new_session = ClassSession(
            title=data["title"],
            description=data.get("description", ""),
            date=datetime.strptime(data["date"], "%d-%m-%Y").date(),
            start_time=datetime.strptime(data["start_time"], "%H:%M").time(),
            end_time=datetime.strptime(data["end_time"], "%H:%M").time(),
            professor_id=data["professor_id"],
            session_type=data["session_type"]
        )
        db.session.add(new_session)
        db.session.commit()
        return success_response("Class session created successfully.", {"id": new_session.id}, 201)
    except Exception as e:
        db.session.rollback()
        return error_response("An error occurred while creating the class session.", 500)

def update_class_session(session_id, data):
    """
    Update an existing class session after validating any changes in schedule.
    """
    session = db.session.get(ClassSession, session_id)
    if session is None:
        abort(404, description="Class session not found for update.")
    date_str = data.get("date", session.date.isoformat())
    start_time_str = data.get("start_time", session.start_time.strftime("%H:%M"))
    end_time_str = data.get("end_time", session.end_time.strftime("%H:%M"))
    session_type = data.get("session_type", session.session_type)
    
    valid, message = is_valid_session_schedule(session_type, date_str, start_time_str, end_time_str)
    if not valid:
        return error_response(message, 400)
    
    try:
        session.title = data.get("title", session.title)
        session.description = data.get("description", session.description)
        if "date" in data:
            session.date = datetime.strptime(data["date"], "%d-%m-%Y").date()
        if "start_time" in data:
            session.start_time = datetime.strptime(data["start_time"], "%H:%M").time()
        if "end_time" in data:
            session.end_time = datetime.strptime(data["end_time"], "%H:%M").time()
        session.professor_id = data.get("professor_id", session.professor_id)
        session.session_type = session_type
        
        db.session.commit()
        return success_response("Class session updated successfully.", {"id": session.id}, 200)
    except Exception as e:
        db.session.rollback()
        return error_response("An error occurred while updating the class session.", 500)

def delete_class_session(session_id):
    """
    Delete a class session.
    """
    session = db.session.get(ClassSession, session_id)
    if session is None:
        abort(404, description="Class session not found for deletion.")
    try:
        db.session.delete(session)
        db.session.commit()
        return success_response("Class session deleted successfully.", {}, 200)
    except Exception as e:
        db.session.rollback()
        return error_response("An error occurred while deleting the class session.", 500)
