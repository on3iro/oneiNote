# -*- coding: utf-8 -*-
"""Api authentication via Flask-JWT."""
from oneiNote.users.models import User
from oneiNote.extensions import jwt


@jwt.authentication_handler
def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user


@jwt.identity_handler
def identity(payload):
    user_id = payload['identity']
    return User.get_by_id(user_id)
