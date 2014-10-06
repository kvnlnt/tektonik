from flask import jsonify, Blueprint, request
from tektonik.models import db, Property


# CONTROLLER
# ==========


controller = Blueprint('property', __name__)


# CRUD
# ====


# create a new property
def properties_create(param):
    record = Property(property=param['property'])
    db.session.add(record)
    db.session.commit()
    payload = jsonify(
        record.serialize(),
        result="OK") if record else jsonify([])
    return payload


# return list of properties
def properties_read():
    properties = Property.query.all()
    data = [i.serialize() for i in properties]
    payload = jsonify(
        data=data,
        result='OK') if data else jsonify([])
    return payload


# bulk update of properties
def properties_update(param):
    id = param['id']
    record = Property.query.get(id)
    record.property = param['property']
    db.session.commit()
    payload = jsonify(
        record.serialize(),
        result="OK") if record else jsonify([])
    return payload


# delete all properties
def properties_delete(param):
    id = param['id']
    record = Property.query.get(id)
    db.session.delete(record)
    db.session.commit()
    payload = jsonify(
        data=[],
        result="DELETED")
    return payload


# get property
def property_read(id):
    record = Property.query.get(id)
    payload = jsonify(
        record.serialize(),
        result="OK") if record else jsonify([])
    return payload


# update a property
def property_update(id, param):
    record = Property.query.get(id)
    record.property = param['property']
    db.session.commit()
    payload = jsonify(
        record.serialize(),
        result="OK") if record else jsonify([])
    return payload


# delete a property
def property_delete(id):
    record = Property.query.get(id)
    db.session.delete(record)
    db.session.commit()
    payload = jsonify(data=[], result="DELETED")
    return payload


# ENDPOINTS
# =========


@controller.route('/properties', methods=['POST', 'GET', 'PUT', 'DELETE'])
def properties():

    if request.method == 'POST':
        return properties_create(request.json)

    if request.method == 'GET':
        return properties_read()

    if request.method == 'PUT':
        return properties_update(request.json)

    if request.method == 'DELETE':
        return properties_delete(request.json)


@controller.route('/properties/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def property(id):

    if request.method == 'GET':
        return property_read(id)

    if request.method == 'PUT':
        return property_update(id, request.json)

    if request.method == 'DELETE':
        return property_delete(id)
