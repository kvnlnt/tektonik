from flask import jsonify, Blueprint, request, redirect, url_for
from validate import validate_json
from tektonik.models import db, Path

controller = Blueprint('path', __name__)


# GET       curl http://127.0.0.1:5000/properties
# POST      curl -i -H "Content-Type: application/json" -X POST -d '{"path":"/home", "property_id":1}' http://127.0.0.1:5000/paths
# DELETE    curl -i -H "Content-Type: application/json" -X DELETE -d '{"path":1}' http://127.0.0.1:5000/paths
@controller.route('/paths', methods=['GET','POST','DELETE'])
@validate_json
def properties():

    if request.method == 'GET':
        paths = Path.query.all()
        data = [i.serialize() for i in paths]
        payload = jsonify(data=data, result='OK') if data else jsonify([])
        return payload

    if request.method == 'POST':
        record = Path(path=request.json['path'], property_id=request.json['property_id'])
        db.session.add(record)
        db.session.commit()
        payload = jsonify(record.serialize(), result="OK") if record else jsonify([])
        return payload

    if request.method == 'DELETE':
        id = request.json['path']
        record = Path.query.get(id)
        db.session.delete(record)
        db.session.commit()
        payload = jsonify(data=[], result="DELETED")
        return payload


# GET       curl http://127.0.0.1:5000/path/1
# PUT       curl -i -H "Content-Type: application/json" -X PUT -d '{"path":"/newpath", "property_id":1}' http://127.0.0.1:5000/path/1
@controller.route('/path/<int:id>', methods=['GET','PUT'])
@validate_json
def property_read_update_delete(id):

    if request.method == 'GET':
        record  = Path.query.get(id)
        payload = jsonify(record.serialize(), result="OK") if record else jsonify([])
        return payload

    if request.method == 'PUT':
        record = Path.query.get(id)
        record.path = request.json['path']
        record.property_id = request.json['property_id']
        db.session.commit()
        payload = jsonify(record.serialize(), result="OK") if record else jsonify([])
        return payload
