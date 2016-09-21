# -*- coding: utf-8 -*-
"""oneiNote API v1.0"""

from flask import Blueprint, jsonify
from flask_restful import Resource, Api, reqparse
from flask_jwt import jwt_required, current_identity

from oneiNote.extensions import marshmallow, csrf_protect
from oneiNote.notes.models import Note

api_blueprint = Blueprint('api_v1', __name__, url_prefix='/api/v1')
api = Api(api_blueprint, decorators=[csrf_protect.exempt])


###########
# Schemas #
###########

class NoteSchema(marshmallow.Schema):
    """Marshmallow schema for the Note model."""
    class Meta:
        # Fields to expose
        fields = ('title', 'content', 'created_at', 'user_id', 'id')


note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)


####################
# Helper Functions #
####################

def get_model_entry_by_id(model_name, model_id):
    """Gets the entry of a certain model by id."""
    model_entry = model_name.query.filter_by(id=model_id).first()

    if model_entry is None:
        raise InvalidAPIUsage('This view does not exist.', status_code=410)
    else:
        return model_entry


#####################
# Custom Exceptions #
#####################

class InvalidAPIUsage(Exception):
    """Class for invalid api usage."""
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
    """Handles invalid api usage and returns error in valid json format."""
    response = jsonify(error.to_dict())
    response.status_code = error.status_code

    return response


#######
# API #
#######


class NoteListAPI(Resource):
    """Shows a list of all ToDos and lets you POST new Notes."""
    method_decorators = [jwt_required()]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title',
                                   type=str,
                                   required=True,
                                   help='No note title provided',
                                   location='json')
        self.reqparse.add_argument('content',
                                   type=str,
                                   default='',
                                   location='json')
        self.reqparse.add_argument('user_id', type=int,
                                   required=True,
                                   help='No user id provided',
                                   location='json')
        super(NoteListAPI, self).__init__()

    def get(self):
        """Get list of Notes for current user."""

        # Get all notes TODO filter for current user
        all_notes = Note.query.all()
        print(current_identity)

        # Serialize notes
        result = notes_schema.dump(all_notes)
        return jsonify(result.data)

    def post(self):
        """Create new note for current user."""

        # Get request arguments
        args = self.reqparse.parse_args()

        # Create new note from arguments
        note = Note(title=args['title'],
                    content=args['content'],
                    user_id=args['user_id'])

        # Save note and return note as json
        if note is not None and note.title != '' and note.user_id != '':
            if note.save():
                result = note_schema.dump(note)
                return jsonify(result.data)
            else:
                raise InvalidAPIUsage('Could not create new note!', 500)
        else:
            raise InvalidAPIUsage('Could not create new note!', 500)


class SingleNoteAPI(Resource):
    """Shows a single Note and lets you edit (PUT) or delete it."""
    decorators = [jwt_required()]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title',
                                   type=str,
                                   required=False,
                                   help='No note title provided',
                                   location='json')
        self.reqparse.add_argument('content',
                                   type=str,
                                   default='',
                                   location='json')
        super(SingleNoteAPI, self).__init__()

    def get(self, note_id):
        """Get note entry by id."""
        note_entry = get_model_entry_by_id(Note, note_id)

        # Serialize note entry
        result = note_schema.dump(note_entry)
        return jsonify(result.data)

    def put(self, note_id):
        """Edit note entry by id."""

        # Get request arguments
        args = self.reqparse.parse_args()

        # Get note by id
        note = get_model_entry_by_id(Note, note_id)

        # Edit note and return note as json
        if note is not None:
            if args['title'] != '':
                note.title = args['title']

            note.content = args['content']
            note.save()

            # Serialize note
            result = note_schema.dump(note)
            return jsonify(result.data)

    def delete(self, note_id):
        """Delete note by id."""
        # Get note
        note = get_model_entry_by_id(Note, note_id)

        # Delete note
        if note is not None:
            note.delete()
            return {"Operation": "Delete", "Status": "successful"}, 200

# TODO tests
# TODO created_at timezone support
# TODO readd CSRF protection for standard urls

# Add Resources
api.add_resource(NoteListAPI,
                 '/',
                 '/notes')
api.add_resource(SingleNoteAPI, '/notes/<int:note_id>')
