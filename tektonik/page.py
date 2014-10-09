from flask import Blueprint
from flask.ext.restful import abort
from flask.ext.restful import Api
from flask.ext.restful import reqparse
from flask.ext.restful import fields
from flask.ext.restful import marshal_with
from flask.ext.restful import Resource
from tektonik.models import db
from tektonik.models import Page as PageModel

# CONTROLLER
# ==========

controller = Blueprint('page', __name__)
api = Api(controller)

# PARSER
# ======

# base parser
parser = reqparse.RequestParser()
parser.add_argument('id', type=int)
parser.add_argument('page', type=str)
parser.add_argument('offset', type=int)
parser.add_argument('limit', type=int)


# FIELDS
# ======

page_fields = {
    'id': fields.Integer,
    'page': fields.String,
}

# RESOURCES
# =========


class Pages(Resource):

    @marshal_with(page_fields)
    def post(self):
        args = parser.parse_args()
        record = PageModel(page=args.page)
        db.session.add(record)
        db.session.commit()
        return record, 201

    @marshal_with(page_fields)
    def get(self):
        records = PageModel.query.all()
        return records, 200


class Page(Resource):

    @marshal_with(page_fields)
    def get(self, id):
        record = PageModel.query.get(id)
        if record:
            return record, 200
        else:
            abort(404, message="Record Not Found")

    @marshal_with(page_fields)
    def put(self, id):
        args = parser.parse_args()
        record = PageModel.query.get(id)
        if record:
            record.page = args.page
            db.session.commit()
            return record, 200
        else:
            abort(404, message="Record Not Found")

    def delete(self, id):
        record = PageModel.query.get(id)
        if record:
            db.session.delete(record)
            db.session.commit()
            return '', 204
        else:
            abort(404, message="Record Not Found")

# ENDPOINTS
# =========

api.add_resource(Pages, '/pages', endpoint='pages')
api.add_resource(Page, '/pages/<int:id>', endpoint='page')
