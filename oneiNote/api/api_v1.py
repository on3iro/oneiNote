# -*- coding: utf-8 -*-
"""oneiNote API v1.0"""

from flask import Blueprint, jsonify
from flask_restful import Resource, Api

from oneiNote.extensions import marshmallow
from oneiNote.notes.models import Note

api_blueprint = Blueprint('api_v1', __name__, url_prefix='/api/v1')
api = Api(api_blueprint)


###########
# Schemas #
###########
class NoteSchema(marshmallow.Schema):
    class Meta:
        # Fields to expose
        fields = ('title', 'content', 'created_at', 'user_id')


note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)


####################
# Helper Functions #
####################

def get_model_entry_by_id(model_name, model_id):
    model_entry = model_name.query.filter_by(id=model_id).first()
    if model_entry is None:
        raise InvalidAPIUsage('This view does not exist.', status_code=410)
    else:
        return model_entry


#####################
# Custom Exceptions #
#####################

class InvalidAPIUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        res = dict(self.payload or ())
        res['message'] = self.message
        return res


#################
# Errorhandlers #
#################

@api_blueprint.errorhandler(InvalidAPIUsage)
def handle_invalid_api_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


#######
# API #
#######

class NoteList(Resource):
    """Shows a list of all ToDos and lets you POST new Notes."""
    def get(self):
        all_notes = Note.query.all()
        result = notes_schema.dump(all_notes)
        return jsonify(result.data)


class SingleNote(Resource):
    """Shows a single Note and lets you edit (PUT) or delete it."""
    def get(self, note_id):
        note_entry = get_model_entry_by_id(Note, note_id)
        result = note_schema.dump(note_entry)
        return jsonify(result.data)


# Add Resources
api.add_resource(NoteList, '/notes')
api.add_resource(SingleNote, '/notes/<note_id>')
