from flask import jsonify, Blueprint, request, redirect, url_for
from functools import wraps
from werkzeug.exceptions import BadRequest
from tektonik.models import db, Property

main = Blueprint('main', __name__)


# VALIDATION

def validate_json(f):
    @wraps(f)
    def wrapper(*args, **kw):
        try:
            request.json
        except BadRequest, e:
            msg = "payload must be a valid json"
            return jsonify({"error": msg}), 400
        return f(*args, **kw)
    return wrapper


# PROPERTIES
# ==========

# GET       curl http://127.0.0.1:5000/properties
@main.route('/properties', methods=['GET'])
@validate_json
def properties():

    properties = Property.query.all()
    data       = [i.serialize() for i in properties]
    payload    = jsonify(data=data, result='OK') if data else jsonify([])

    return payload


# POST      curl -i -H "Content-Type: application/json" -X POST -d '{"property":"kevinlint.com"}' http://127.0.0.1:5000/property
@main.route('/property', methods=['POST'])
@validate_json
def property_create():

    record  = Property(property=request.json['property'])
    payload = jsonify(record.serialize(), result="OK") if record else jsonify([])

    db.session.add(record)
    db.session.commit()

    return payload


# GET       curl http://127.0.0.1:5000/property/1
# PUT       curl -i -H "Content-Type: application/json" -X PUT -d '{"property":"kevinlint.com"}' http://127.0.0.1:5000/property/1
# DELETE `  curl -i -H "Content-Type: application/json" -X DELETE -d "key=value" http://127.0.0.1:5000/property/1
@main.route('/property/<int:id>', methods=['GET','PUT','DELETE'])
@validate_json
def property_read_update_delete(id):

    if request.method == 'GET':
        record  = Property.query.get(id)
        payload = jsonify(record.serialize(), result="OK") if record else jsonify([])
        return payload

    if request.method == 'PUT':
        record = Property.query.get(id)
        record.property = request.json['property']
        payload = jsonify(record.serialize(), result="OK") if record else jsonify([])
        db.session.commit()
        return payload

    if request.method == 'DELETE':
        record = Property.query.get(id)
        payload = jsonify(record.serialize(), result="OK") if record else jsonify([])
        db.session.delete(record)
        db.session.commit()
        return payload
