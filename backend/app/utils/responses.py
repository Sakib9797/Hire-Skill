from flask import jsonify

def success_response(data=None, message='Success', status=200):
    """Generate a success response"""
    response = {
        'success': True,
        'message': message
    }
    if data is not None:
        response['data'] = data
    return jsonify(response), status

def error_response(message='Error occurred', status=400, errors=None):
    """Generate an error response"""
    response = {
        'success': False,
        'message': message
    }
    if errors:
        response['errors'] = errors
    return jsonify(response), status

def validation_error_response(errors):
    """Generate a validation error response"""
    return error_response(
        message='Validation failed',
        status=422,
        errors=errors
    )
