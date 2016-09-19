# -*- coding: utf-8 -*-
"""Views for notes."""
from flask import Blueprint

notes_blueprint = Blueprint('notes', __name__, url_prefix='/notes',
                            static_folder='../static')
