import datetime as dt
from flask import Blueprint
from flask.ext.restful import abort
from flask.ext.restful import Api
from flask.ext.restful import reqparse
from flask.ext.restful import fields
from flask.ext.restful import marshal_with
from flask.ext.restful import Resource
from tektonik.models import db
from tektonik.models import PathPage as PathPageModel

# CONTROLLER
# ==========

controller = Blueprint('path_page', __name__)
api = Api(controller)

# PARSER
# ======

# base parser
parser = reqparse.RequestParser()
parser.add_argument('id', type=int)
parser.add_argument('path_id', type=int, required=True)
parser.add_argument('page_id', type=int, required=True)
parser.add_argument('effective_date', type=dt, default=dt.datetime.now())
parser.add_argument('expiration_date', type=dt, default=None)


# FIELDS
# ======

fields = {
    'id': fields.Integer,
    'path_id': fields.Integer,
    'page_id': fields.Integer,
    'effective_date': fields.DateTime,
    'expiration_date': fields.DateTime,
}

# RESOURCES
# =========


class PathPages(Resource):

    @marshal_with(fields)
    def post(self):
        args = parser.parse_args()
        record = PathPageModel(
            path_id=args.path_id,
            page_id=args.page_id,
            effective_date=args.effective_date,
            expiration_date=args.expiration_date
        )
        db.session.add(record)
        db.session.commit()
        return record, 201

    @marshal_with(fields)
    def get(self):
        records = PathPageModel.query.all()
        return records, 200


class PathPage(Resource):

    @marshal_with(fields)
    def get(self, id):
        record = PathPageModel.query.get(id)
        if record:
            return record, 200
        else:
            abort(404, message="Record Not Found")

    @marshal_with(fields)
    def put(self, id):
        args = parser.parse_args()
        record = PathPageModel.query.get(id)
        if record:
            record.path_id = args.path_id
            record.page_id = args.page_id
            record.effective_date = args.effective_date
            record.expiration_date = args.expiration_date
            db.session.commit()
            return record, 200
        else:
            abort(404, message="Record Not Found")

    def delete(self, id):
        record = PathPageModel.query.get(id)
        if record:
            db.session.delete(record)
            db.session.commit()
            return '', 204
        else:
            abort(404, message="Record Not Found")

# ENDPOINTS
# =========

api.add_resource(PathPages, '/path-pages', endpoint='path_pages')
api.add_resource(PathPage, '/path-pages/<int:id>', endpoint='path_page')
