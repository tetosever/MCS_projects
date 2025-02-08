from flask import jsonify, request, current_app, Blueprint, render_template
from flask_app.app.blueprints.exceptions.exceptions import ValidationError

error_bp = Blueprint('error', __name__)

@error_bp.route('/error')
def error_page():
    status_code = request.args.get("code", "500")
    message = request.args.get("message", "Si è verificato un errore imprevisto")

    return render_template("error.html", status_code=status_code, message=message), int(status_code)

def handle_validation_error(error):
    return render_error(400, error.message)

def handle_value_error(error):
    return render_error(400, str(error))

def handle_authentication_error(error):
    return render_error(401, "Autenticazione fallita")

def handle_permission_denied_error(error):
    return render_error(403, "Accesso negato")

def handle_not_found(error):
    return render_error(404, "Risorsa non trovata")

def handle_internal_error(error):
    return render_error(500, "Errore interno del server")

def handle_generic_error(error):
    """
    Catch-all handler for unexpected errors.
    """
    message = str(error) if current_app.config.get("DEBUG", False) else "Si è verificato un errore imprevisto"
    return render_error(500, message)

def render_error(status_code, message):
    """
    Returns a JSON error response for all requests.
    """
    response = jsonify({
        "error": True,
        "status_code": status_code,
        "message": message
    })
    response.status_code = status_code
    return response

def register_error_handlers(app):
    """
    Registers global error handlers.
    """
    app.register_error_handler(ValidationError, handle_validation_error)
    app.register_error_handler(400, handle_value_error)
    app.register_error_handler(404, handle_not_found)
    app.register_error_handler(500, handle_internal_error)
    app.register_error_handler(Exception, handle_generic_error)  # Catch-all handler
