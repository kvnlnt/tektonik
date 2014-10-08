from flask import Blueprint
from flask.ext.restful import abort
from flask.ext.restful import Api
from flask.ext.restful import reqparse
from flask.ext.restful import fields
from flask.ext.restful import marshal_with
from flask.ext.restful import Resource
from tektonik.models import db
from tektonik.models import Path as PathModel

# CONTROLLER
# ==========

controller = Blueprint('path', __name__)
api = Api(controller)

# PARSER
# ======

# base parser
parser = reqparse.RequestParser()
parser.add_argument('id',
                    type=int,
                    location='json',
                    help='Invalid ID')
parser.add_argument('path',
                    type=str,
                    location='json',
                    help='Invalid Path')
parser.add_argument('property_id',
                    type=int,
                    location='json',
                    help='Invalid Property ID')
parser.add_argument('offset',
                    type=int,
                    location='args')
parser.add_argument('limit',
                    type=int,
                    location='args')

# we need to require the property id for individual put records
pathParser = parser.copy()
pathParser.replace_argument('property_id',
                            type=int,
                            location='json',
                            help='Invalid Property ID',
                            required=True)

# FIELDS
# ======

path_fields = {
    'id': fields.Integer,
    'path': fields.String,
    'property_id': fields.Integer,
}

# RESOURCES
# =========


class Paths(Resource):

    @marshal_with(path_fields)
    def post(self):
        args = parser.parse_args()
        record = PathModel(path=args.path, property_id=args.property_id)
        db.session.add(record)
        db.session.commit()
        return record, 201

    @marshal_with(path_fields)
    def get(self):
        records = PathModel.query.all()
        return records, 200


class Path(Resource):

    @marshal_with(path_fields)
    def get(self, id):
        try:
            record = PathModel.query.get(id)
            if record:
                return record, 200
            else:
                raise LookupError("Record Not Found")
        except LookupError as e:
            abort(404, message=str(e))

    @marshal_with(path_fields)
    def put(self, id):
        try:
            args = pathParser.parse_args()
            record = PathModel.query.get(id)
            if record:
                record.path = args.path
                record.property_id = args.property_id
                db.session.commit()
                return record, 200
            else:
                raise LookupError("Record Not Found")
        except LookupError as e:
            abort(404, message=str(e))

    def delete(self, id):
        try:
            record = PathModel.query.get(id)
            if record:
                db.session.delete(record)
                db.session.commit()
                return '', 204
            else:
                raise LookupError("Record Not Found")
        except LookupError as e:
            abort(404, message=str(e))

# ENDPOINTS
# =========

api.add_resource(Paths, '/paths', endpoint='paths')
api.add_resource(Path, '/paths/<int:id>', endpoint='path')
