from flask import jsonify, Blueprint, request, redirect, url_for
from functools import wraps
from werkzeug.exceptions import BadRequest
from tektonik.models import db, Property, Path

main = Blueprint('main', __name__)


# VALIDATION
# ==========

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
# POST      curl -i -H "Content-Type: application/json" -X POST -d '{"property":"kevinlint.com"}' http://127.0.0.1:5000/properties
@main.route('/properties', methods=['GET','POST'])
@validate_json
def properties():

    if request.method == 'GET':
        properties = Property.query.all()
        data = [i.serialize() for i in properties]
        payload = jsonify(data=data, result='OK') if data else jsonify([])
        return payload

    if request.method == 'POST':
        record = Property(property=request.json['property'])
        db.session.add(record)
        db.session.commit()
        payload = jsonify(record.serialize(), result="OK") if record else jsonify([])
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
        db.session.commit()
        payload = jsonify(record.serialize(), result="OK") if record else jsonify([])
        return payload

    if request.method == 'DELETE':
        record = Property.query.get(id)
        db.session.delete(record)
        db.session.commit()
        payload = jsonify(data=[], result="DELETED")
        return payload


# # PATHS
# # =====

# # GET       curl http://127.0.0.1:5000/paths
# @main.route('/paths', methods=['GET'])
# @validate_json
# def paths():

#     paths   = Path.query.all()
#     data    = [i.serialize() for i in paths]
#     payload = jsonify(data=data, result='OK') if data else jsonify([])
#     return payload

# # POST      curl -i -H "Content-Type: application/json" -X POST -d '{"property":"kevinlint.com"}' http://127.0.0.1:5000/path
# @main.route('/path', methods=['POST'])
# @validate_json
# def path_create():

#     record  = Path(path=request.json['path'], property_id=request.json['property_id'])
#     db.session.add(record)
#     db.session.commit()
#     payload = jsonify(record.serialize(), result="OK") if record else jsonify([])
#     return payload


# # GET       curl http://127.0.0.1:5000/path/1
# # PUT       curl -i -H "Content-Type: application/json" -X PUT -d '{"page":"kevinlint.com"}' http://127.0.0.1:5000/path/1
# # DELETE `  curl -i -H "Content-Type: application/json" -X DELETE -d "key=value" http://127.0.0.1:5000/path/1
# @main.route('/path/<int:id>', methods=['GET','PUT','DELETE'])
# @validate_json
# def path_read_update_delete(id):

#     if request.method == 'GET':
#         record  = Path.query.get(id)
#         payload = jsonify(record.serialize(), result="OK") if record else jsonify([])
#         return payload

#     if request.method == 'PUT':
#         record = Path.query.get(id)
#         record.path = request.json['path']
#         record.property = request.json['path']
#         db.session.commit()
#         payload = jsonify(record.serialize(), result="OK") if record else jsonify([])
#         return payload

#     if request.method == 'DELETE':
#         record = Path.query.get(id)
#         db.session.delete(record)
#         db.session.commit()
#         payload = jsonify(data=[], result="DELETED")
#         return payload


# # PAGES
# # =====

# # GET       curl http://127.0.0.1:5000/pages
# @main.route('/pages', methods=['GET'])
# @validate_json
# def pages():

#     pages   = Page.query.all()
#     data    = [i.serialize() for i in pages]
#     payload = jsonify(data=data, result='OK') if data else jsonify([])
#     return payload

# # POST      curl -i -H "Content-Type: application/json" -X POST -d '{"property":"kevinlint.com"}' http://127.0.0.1:5000/page
# @main.route('/page', methods=['POST'])
# @validate_json
# def page_create():

#     record  = Page(page=request.json['page'])
#     db.session.add(record)
#     db.session.commit()
#     payload = jsonify(record.serialize(), result="OK") if record else jsonify([])
#     return payload


# # GET       curl http://127.0.0.1:5000/page/1
# # PUT       curl -i -H "Content-Type: application/json" -X PUT -d '{"page":"kevinlint.com"}' http://127.0.0.1:5000/page/1
# # DELETE `  curl -i -H "Content-Type: application/json" -X DELETE -d "key=value" http://127.0.0.1:5000/page/1
# @main.route('/page/<int:id>', methods=['GET','PUT','DELETE'])
# @validate_json
# def page_read_update_delete(id):

#     if request.method == 'GET':
#         record  = Page.query.get(id)
#         payload = jsonify(record.serialize(), result="OK") if record else jsonify([])
#         return payload

#     if request.method == 'PUT':
#         record = Page.query.get(id)
#         record.page = request.json['page']
#         db.session.commit()
#         payload = jsonify(record.serialize(), result="OK") if record else jsonify([])
#         return payload

#     if request.method == 'DELETE':
#         record = Page.query.get(id)
#         db.session.delete(record)
#         db.session.commit()
#         payload = jsonify(record.serialize(), result="OK") if record else jsonify([])
#         return payload
