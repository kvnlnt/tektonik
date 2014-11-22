from flask import jsonify
from flask import request
from tektonik.models import db
from tektonik.models import Property
from tektonik.schemas import Property as PropertySchema
from tektonik.v1_0 import api


@api.route("/properties", methods=['GET'])
def get_properties():
    properties = Property.query.all()
    schema = PropertySchema(many=True)
    result, errors = schema.dump(properties)

    if errors:
        return jsonify({"result": errors}), 404
    else:
        return jsonify({"result": result}), 200


@api.route("/properties", methods=['POST'])
def create_property():

    schema = PropertySchema()
    result, errors = schema.load(request.json)

    if errors:
        return jsonify({"result": errors}), 403
    else:
        record = Property(property=result['property'])
        db.session.add(record)
        db.session.commit()
        return jsonify({"result": result}), 200
