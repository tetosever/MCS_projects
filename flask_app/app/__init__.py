from flask import Flask

from flask_app.app.blueprints.exceptions import create_exception_blueprint
from flask_app.app.blueprints.views import create_views_blueprint
from flask_app.app.blueprints.api import create_api_blueprint

def create_app():
    app = Flask(__name__)

    app.register_blueprint(create_views_blueprint(), url_prefix='/')
    app.register_blueprint(create_api_blueprint(), url_prefix='/api')
    app.register_blueprint(create_exception_blueprint())

    return app
