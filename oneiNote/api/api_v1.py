# -*- coding: utf-8 -*-
"""oneiNote API v1.0"""

from flask import Blueprint

from oneiNote.database import db
from oneiNote.notes.models import Note

api_blueprint = Blueprint('api_v1', __name__, url_prefix='/api/v1')

