"""
:synopsis: Properties controller
"""

from flask import Blueprint
from flask import jsonify
from flask import request
from tektonik.models import db
from tektonik.models.property import Property as PropertyModel
from tektonik.schemas.property import property_schema_list
from tektonik.schemas.property import property_schema_read
from tektonik.schemas.property import property_schema

blueprint = Blueprint('properties', __name__)


@blueprint.route("", methods=['GET'])
def list_properties():

    """ list properties """

    properties = PropertyModel.query.all()
    result, errors = property_schema_list.dump(properties)
    metadata = {"total_records": PropertyModel.query.count()}

    if errors:
        return jsonify({"result": errors}), 404
    else:
        return jsonify({"result": result, "metadata": metadata}), 200


@blueprint.route("", methods=['POST'])
def create_property():

    """ create new property """

    result, errors = property_schema.load(request.json)

    if errors:
        return jsonify({"errors": errors}), 403
    else:
        record = PropertyModel(property=result['property'])
        db.session.add(record)
        db.session.commit()
        record = property_schema.dump(record).data
        return jsonify(
            {"result":
                {"record": record,
                 "message": "Property successfully added"}}), 201


@blueprint.route("/<int:id>", methods=['GET'])
def read_property(id):

    """ get property details """

    record = PropertyModel.query.get(id)
    result, errors = property_schema_read.dump(record)

    if not record:
        return jsonify({"result": "Record not found"}), 404
    else:
        return jsonify({"result": result}), 200


@blueprint.route("/<int:id>", methods=['PUT', 'PATCH'])
def update_property(id):

    """ update property """

    record = PropertyModel.query.get(id)
    request.json['id'] = id
    result, errors = property_schema.load(request.json)

    if errors:
        return jsonify({"errors": errors}), 403
    else:
        record.property = result['property']
        db.session.commit()
        record = property_schema.dump(record).data
        return jsonify({"result": record}), 200


@blueprint.route("/<int:id>", methods=['DELETE'])
def delete_property(id):

    """ delete property """

    record = PropertyModel.query.get(id)
    result, errors = property_schema.dump(record)

    if not record:
        return jsonify({"result": "Record not found"}), 403
    else:
        db.session.delete(record)
        db.session.commit()
        return jsonify({"result": result}), 200
