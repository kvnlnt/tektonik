from flask import Blueprint
from flask import jsonify
from flask.ext.restful import abort
from flask.ext.restful import Api
from flask.ext.restful import fields
from flask.ext.restful import marshal_with
from flask.ext.restful import marshal
from flask.ext.restful import reqparse
from flask.ext.restful import Resource
from flask_restful.utils import cors
from tektonik.models import db
from tektonik.models import Property as PropertyModel
from tektonik.validate import Validate

# CONTROLLER
# ==========

controller = Blueprint('property_1.0', __name__)
api = Api(controller)

# DECORATORS
# ==========

api.decorators = [cors.crossdomain(origin='*', headers='Content-Type')]

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


def make_error(status_code, error):
    response = jsonify({'error': error})
    response.status_code = status_code
    return response


class Properties(Resource):

    def post(self):
        args = parser.parse_args()
        print "============================================"
        record = PropertyModel(property=args.property)
        if record:
            db.session.add(record)
            db.session.commit()
            return marshal(record, property_fields), 201
        else:
            return make_error(403, 'broken')

    def get(self):
        records = PropertyModel.query.all()
        if records:
            return marshal(records, property_fields), 200
        else:
            return make_error(404, 'No Records Found')

    def options(self):
        pass


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
            return make_error(404, 'Record Not Found')

    def options(self):
        pass

# ENDPOINTS
# =========

api.add_resource(Properties, '/properties', endpoint='properties')
api.add_resource(Property, '/properties/<int:id>', endpoint='property')
