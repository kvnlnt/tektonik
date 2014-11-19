from flask import Blueprint
from flask.ext.restful import abort
from flask.ext.restful import Api
from flask.ext.restful import fields
from flask.ext.restful import marshal_with
from flask.ext.restful import reqparse
from flask.ext.restful import Resource
from flask_restful.utils import cors
from tektonik.models import db
from tektonik.models import Property as PropertyModel
from tektonik.validate import Validate

# CONTROLLER
# ==========

controller = Blueprint('property', __name__)
api = Api(controller)

# DECORATORS
# ==========

api.decorators = [cors.crossdomain(origin='*')]

# PARSER
# ======

# base parser
parser = reqparse.RequestParser()
parser.add_argument('id', type=int)
parser.add_argument(
    'property',
    type=Validate.property,
    required=True
)
parser.add_argument('offset', type=int)
parser.add_argument('limit', type=int)


# FIELDS
# ======

property_fields = {
    'id': fields.Integer,
    'property': fields.String,
}

# RESOURCES
# =========


class Properties(Resource):

    @marshal_with(property_fields)
    def post(self):
        args = parser.parse_args()
        record = PropertyModel(property=args.property)
        db.session.add(record)
        db.session.commit()
        return record, 201

    @marshal_with(property_fields)
    def get(self):
        records = PropertyModel.query.all()
        if records:
            return records, 200
        else:
            abort(404, message="No Records Found")


class Property(Resource):

    @marshal_with(property_fields)
    def get(self, id):
        record = PropertyModel.query.get(id)
        if record:
            return record, 200
        else:
            abort(404, message="Record Not Found")

    @marshal_with(property_fields)
    def put(self, id):
        args = parser.parse_args()
        record = PropertyModel.query.get(id)
        if record:
            record.property = args.property
            db.session.commit()
            return record, 200
        else:
            abort(404, message="Record Not Found")

    def delete(self, id):
        record = PropertyModel.query.get(id)
        if record:
            db.session.delete(record)
            db.session.commit()
            return '', 204
        else:
            abort(404, message="Record Not Found")

    def options(self):
        pass

# ENDPOINTS
# =========

api.add_resource(Properties, '/properties', endpoint='properties')
api.add_resource(Property, '/properties/<int:id>', endpoint='property')
