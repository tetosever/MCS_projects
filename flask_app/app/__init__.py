from flask import Flask

from flask_app.app.blueprints.exceptions import create_error_blueprint
from flask_app.app.blueprints.exceptions.exception_handler import register_error_handlers
from flask_app.app.blueprints.exceptions.exception_handler import handle_validation_error, handle_value_error, \
    handle_not_found, handle_internal_error, handle_generic_error
from flask_app.app.blueprints.exceptions.exceptions import ValidationError
from flask_app.app.blueprints.views import create_views_blueprint
from flask_app.app.blueprints.api import create_api_blueprint

def create_app():
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["TRAP_HTTP_EXCEPTIONS"] = True

    register_error_handlers(app)
    app.register_blueprint(create_views_blueprint(), url_prefix='/')
    app.register_blueprint(create_api_blueprint(), url_prefix='/api')
    app.register_blueprint(create_error_blueprint())

    return app
