from flask import jsonify, Blueprint, request, redirect, url_for
from validate import validate_json
from tektonik.models import db, Property

controller = Blueprint('property', __name__)

# CRUD
# ====

def property_create(param):
    record = Property(property=param['property'])
    db.session.add(record)
    db.session.commit()
    payload = jsonify(record.serialize(), result="OK") if record else jsonify([])
    return payload


def property_read_list():
    properties = Property.query.all()
    data = [i.serialize() for i in properties]
    payload = jsonify(data=data, result='OK') if data else jsonify([])
    return payload


def property_read(id):
    record = Property.query.get(id)
    payload = jsonify(record.serialize(), result="OK") if record else jsonify([])
    return payload


def property_update(param):
    id = param['id']
    record = Property.query.get(id)
    record.property = param['property']
    db.session.commit()
    payload = jsonify(record.serialize(), result="OK") if record else jsonify([])
    return payload


def property_delete(param):
    id = param['id']
    record = Property.query.get(id)
    db.session.delete(record)
    db.session.commit()
    payload = jsonify(data=[], result="DELETED")
    return payload


# ENDPOINTS
# =========

# POST      curl -i -H "Content-Type: application/json" -X POST -d '{"property":"kevinlint.com"}' http://127.0.0.1:5000/properties
# GET       curl http://127.0.0.1:5000/properties
# PUT       curl -i -H "Content-Type: application/json" -X PUT -d '{"id":1, "property":"updated"}' http://127.0.0.1:5000/properties
# DELETE    curl -i -H "Content-Type: application/json" -X DELETE -d '{"id":14}' http://127.0.0.1:5000/properties
@controller.route('/properties', methods=['POST','GET','PUT','DELETE'])
@validate_json
def properties():
    
    if request.method == 'POST':
        return property_create(request.json)

    if request.method == 'GET':
        return property_read_list()

    if request.method == 'PUT':
        return property_update(request.json)

    if request.method == 'DELETE':
        return property_delete(request.json)

# GET       curl http://127.0.0.1:5000/property/:id
@controller.route('/properties/<int:id>', methods=['GET'])
@validate_json
def property(id):

    if request.method == 'GET':
        return property_read(id)
