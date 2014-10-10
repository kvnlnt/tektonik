from flask import Blueprint
from flask.ext.restful import abort
from flask.ext.restful import Api
from flask.ext.restful import reqparse
from flask.ext.restful import fields
from flask.ext.restful import marshal_with
from flask.ext.restful import Resource
from tektonik.models import db
from tektonik.models import Path as PathModel
from tektonik.models import PathPage as PathPageModel

# CONTROLLER
# ==========

controller = Blueprint('path', __name__)
api = Api(controller)

# PARSER
# ======


def page_validation(value, name):
    return value


# base parser
parser = reqparse.RequestParser()
parser.add_argument('id', type=int)
parser.add_argument('path', type=str, default="/")
parser.add_argument('property_id', type=int)
parser.add_argument('pages', type=page_validation, default=[])
parser.add_argument('offset', type=int)
parser.add_argument('limit', type=int)

# we need to require the property id for individual put records
pathParser = parser.copy()
pathParser.replace_argument('property_id', type=int, required=True)

# FIELDS
# ======

path_fields = {
    'id': fields.Integer,
    'page': fields.String
}

path_page_fields = {
    'id': fields.Integer,
    'path_id': fields.Integer,
    'page_id': fields.Integer,
    'effective_date': fields.DateTime,
    'expiration_date': fields.DateTime,
    'page': fields.Nested(path_fields)
}

path_fields = {
    'id': fields.Integer,
    'path': fields.String,
    'property_id': fields.Integer,
    'pages': fields.List(fields.Nested(path_page_fields))
}

# RESOURCES
# =========


class Paths(Resource):

    @marshal_with(path_fields)
    def post(self):
        args = parser.parse_args()

        # create new path
        path = PathModel(path=args.path, property_id=args.property_id)
        db.session.add(path)
        db.session.commit()

        # add all pages to path_pages
        for page in args.pages:
            path_page = PathPageModel(path_id=path.id, page_id=page['id'])
            db.session.add(path_page)
            db.session.commit()

        return path, 201

    @marshal_with(path_fields)
    def get(self):
        records = PathModel.query.all()
        return records, 200


class Path(Resource):

    @marshal_with(path_fields)
    def get(self, id):
        record = PathModel.query.get(id)
        if record:
            return record, 200
        else:
            abort(404, message="Record Not Found")

    @marshal_with(path_fields)
    def put(self, id):
        args = pathParser.parse_args()
        path = PathModel.query.get(id)
        if path:

            path.path = args.path
            path.property_id = args.property_id
            db.session.commit()

            # delete path pages
            PathPageModel.query.filter_by(path_id=id).delete()
            db.session.commit()

            # add all pages to path_pages
            for page in args.pages:
                path_page = PathPageModel(path_id=path.id, page_id=page['id'])
                db.session.add(path_page)
                db.session.commit()

            return path, 200
        else:
            abort(404, message="Record Not Found")

    def delete(self, id):
        record = PathModel.query.get(id)
        if record:
            db.session.delete(record)
            db.session.commit()
            return '', 204
        else:
            abort(404, message="Record Not Found")

# ENDPOINTS
# =========

api.add_resource(Paths, '/paths', endpoint='paths')
api.add_resource(Path, '/paths/<int:id>', endpoint='path')
