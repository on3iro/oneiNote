# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask, render_template, jsonify
from flask_admin import Admin
from flask_jwt import JWTError
from collections import OrderedDict

from oneiNote.settings import ProdConfig
from oneiNote.extensions import bcrypt, csrf_protect, db, migrate, \
    login_manager, debug_tb, marshmallow, jwt
from oneiNote.main.views import main_blueprint
from oneiNote.admin.views import MyModelView, MyAdminIndexView, \
    UserView, NotesView
from oneiNote.users.views import users_blueprint
from oneiNote.users.models import User, Role
from oneiNote.notes.views import notes_blueprint
from oneiNote.notes.models import Note
from oneiNote.api.api_v1 import api_blueprint


def create_app(config_object=ProdConfig):
    """An application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories.

    :param config_object: The configuration object to use.
    """

    app = Flask(__name__)
    app.config.from_object(config_object)
    register_blueprints(app)
    register_extensions(app)
    register_errorhandlers(app)
    init_admin(app)

    # Propagate JWTErrors through Flask-RESTful
    # app.handle_user_exception = handle_user_exception_again
    return app


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Flask JWT
    from oneiNote.api.auth import authenticate, identity
    jwt.init_app(app)

    db.init_app(app)
    csrf_protect.init_app(app)
    migrate.init_app(app, db)
    debug_tb.init_app(app)
    marshmallow.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(users_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(notes_blueprint)
    app.register_blueprint(api_blueprint)
    return None


def register_errorhandlers(app):
    """Register error handlers."""

    for errcode in [401, 404, 500]:
        app.register_error_handler(errcode, render_error)

    return None


def init_admin(app):
    """Adds ModelViews to flask-admin."""
    admin = Admin(
        app,
        name="oneiNote-Admin",
        index_view=MyAdminIndexView(),
        base_template='my_master.html',
        endpoint="admin"
    )
    admin.add_view(MyModelView(Role, db.session))
    admin.add_view(UserView(User, db.session))
    admin.add_view(NotesView(Note, db.session))

    return None


####################
# Helper functions #
####################

def render_error(error):
    """Render error template"""
    # If a HTTPException, pull the `code` attribute; default to 500
    error_code = getattr(error, 'code', 500)

    error_code = parse_401_to_404(error_code)

    return render_template('{0}.html'.format(error_code)), error_code


def parse_401_to_404(error_code):
    """Parses a 401 error code to a 404."""

    # The user does not need to know that he is not
    # allowed to access a certain
    # resource. For security reasons the user should see the standard
    # 404 instead of an unauthorized error
    if error_code == 401:
        error_code = 404

    return error_code


def handle_user_exception_again(e):
    """Propagates JWTErrors through Flask-RESTFul."""
    if isinstance(e, JWTError):
        return jsonify(OrderedDict([
            ('status_code', e.status_code),
            ('error', e.error),
            ('description', e.description),
        ])), e.status_code, e.headers
    return e
