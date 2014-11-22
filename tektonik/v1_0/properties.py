from tektonik.v1_0 import api
from tektonik.models import Property, PropertySchema
from flask import jsonify


@api.route("/properties", methods=['GET'])
def get_properties():
    properties = Property.query.all()
    serializer = PropertySchema(many=True)
    result = serializer.dump(properties)
    if properties:
        return jsonify({"results": result.data}), 200
    else:
        return jsonify({"results": "No records found"}), 404
