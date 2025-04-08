from flask import jsonify

def success_response(message, data, status_code):
    """Format a success response with a message and data."""
    response = {
        "message": message,
        "data": data
    }
    return jsonify(response), status_code

def error_response(message, status_code):
    """Format an error response with a message."""
    response = {
        "error": message
    }
    return jsonify(response), status_code
