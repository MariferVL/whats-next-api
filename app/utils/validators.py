from datetime import datetime, time

def is_valid_session_schedule(session_type, session_date_str, start_time_str, end_time_str):
    """
    Validates the session schedule based on the session type.

    For regular classes ("class"):
      - Must be scheduled from Monday to Thursday.
      - Time must be between 10:00 and 12:00 (Chile Time).

    For Q&A sessions ("qa"):
      - Typically scheduled on Fridays.
      - You can enforce Friday or allow flexibility based on your needs.

    For demo sessions ("demo"):
      - Typically scheduled on Fridays.
      - You can enforce Friday or allow flexibility based on your needs.
      
    Returns a tuple: (bool, message).
    """
    try:
        session_date = datetime.strptime(session_date_str, "%d-%m-%Y").date()
        start_time_obj = datetime.strptime(start_time_str, "%H:%M").time()
        end_time_obj = datetime.strptime(end_time_str, "%H:%M").time()
    except ValueError:
        return False, "Invalid date or time format. Please use 'DD-MM-YYYY' for dates and 'HH:MM' for times."
    
    session_type = session_type.lower()
    if session_type == "class":
        # Regular classes: Monday (0) to Thursday (3)
        if session_date.weekday() not in [0, 1, 2, 3]:
            return False, "Regular classes can only be scheduled from Monday to Thursday."
        valid_start, valid_end = time(10, 0), time(12, 0)
        if not (valid_start <= start_time_obj < valid_end and valid_start < end_time_obj <= valid_end):
            return False, "Regular classes must be scheduled between 10:00 and 12:00 Chile Time."
    elif session_type == "qa":
        # Q&A sessions: for example, enforce Fridays (weekday 4)
        if session_date.weekday() != 4:
            return False, "Q&A sessions are typically scheduled on Fridays."
    elif session_type == "demo":
        # Demo sessions: for example, enforce Fridays (weekday 4)
        if session_date.weekday() != 4:
            return False, "Demo sessions are typically scheduled on Fridays."
    
    return True, ""
