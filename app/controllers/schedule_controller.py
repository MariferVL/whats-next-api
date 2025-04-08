from datetime import datetime
from app.models import ClassSession

def get_schedule_for_date(date_str):
    """
    Retrieve class sessions for the specified date.
    Returns a tuple: (sessions, error_message).
    """
    try:
        query_date = datetime.strptime(date_str, "%d-%m-%Y").date()
    except ValueError:
        return None, "Invalid date format. Use DD-MM-YYYY."
    
    sessions = ClassSession.query.filter_by(date=query_date).all()
    return sessions, ""
