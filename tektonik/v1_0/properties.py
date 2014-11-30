"""
:synopsis: Properties controller
"""

from flask import jsonify
from flask import request
from tektonik.models import db
from tektonik.models import Property as PropertyModel
from tektonik.schemas import Property as PropertySchema
from tektonik.v1_0 import api


@api.route("/properties", methods=['POST'])
def create_property():
    """ create new property """

    schema = PropertySchema()
    result, errors = schema.load(request.json)

    if errors:
        return jsonify({"errors": errors}), 403
    else:
        record = PropertyModel(property=result['property'])
        db.session.add(record)
        db.session.commit()
        record = schema.dump(record).data
        return jsonify({"result": record}), 201


@api.route("/properties", methods=['GET'])
def read_properties():

    properties = PropertyModel.query.all()
    schema = PropertySchema(many=True)
    result, errors = schema.dump(properties)

    if errors:
        return jsonify({"result": errors}), 404
    else:
        return jsonify({"result": result}), 200


@api.route("/properties/<int:id>", methods=['GET'])
def read_property(id):

    record = PropertyModel.query.get(id)
    schema = PropertySchema()
    result, errors = schema.dump(record)

    if not record:
        return jsonify({"result": "Record not found"}), 404
    else:
        return jsonify({"result": result}), 200


@api.route("/properties/<int:id>", methods=['PUT', 'PATCH'])
def update_property(id):

    record = PropertyModel.query.get(id)
    schema = PropertySchema(strict=True)
    result, errors = schema.dump(request.json)

    if errors:
        return jsonify({"result": errors}), 403
    else:
        record.property = result['property']
        db.session.commit()
        record = schema.dump(record).data
        return jsonify(record), 200


@api.route("/properties/<int:id>", methods=['DELETE'])
def delete_property(id):

    record = PropertyModel.query.get(id)
    schema = PropertySchema()
    result, errors = schema.dump(record)

    if not record:
        return jsonify({"result": "Record not found"}), 403
    else:
        db.session.delete(record)
        db.session.commit()
        return jsonify({"result": result}), 200
