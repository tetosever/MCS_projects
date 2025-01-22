from flask import Blueprint, jsonify

from flask_app.app.blueprints.exceptions.exceptions import ValidationError

exception = Blueprint('exception', __name__)

@exception.errorhandler(ValidationError)
def handle_validation_error(error):
    response = jsonify({"errors": error.errors})
    response.status_code = error.status_code
    return response

@exception.errorhandler(404)
def handle_not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@exception.errorhandler(500)
def handle_internal_error(error):
    return jsonify({"error": "Internal server error"}), 500
