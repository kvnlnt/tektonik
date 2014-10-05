from flask import jsonify, Blueprint, request, redirect, url_for
from validate import validate_json
from tektonik.models import db, Page

controller = Blueprint('page', __name__)


# GET       curl http://127.0.0.1:5000/pages
# POST      curl -i -H "Content-Type: application/json" -X POST -d '{"page":"home", "page_id":1}' http://127.0.0.1:5000/pages
# DELETE    curl -i -H "Content-Type: application/json" -X DELETE -d '{"page":1}' http://127.0.0.1:5000/pages
@controller.route('/pages', methods=['GET','POST','DELETE'])
@validate_json
def page():

    if request.method == 'GET':
        pages = Page.query.all()
        data = [i.serialize() for i in pages]
        payload = jsonify(data=data, result='OK') if data else jsonify([])
        return payload

    if request.method == 'POST':
        record = Page(page=request.json['page'])
        db.session.add(record)
        db.session.commit()
        payload = jsonify(record.serialize(), result="OK") if record else jsonify([])
        return payload

    if request.method == 'DELETE':
        id = request.json['page']
        record = Page.query.get(id)
        db.session.delete(record)
        db.session.commit()
        payload = jsonify(data=[], result="DELETED")
        return payload


# GET       curl http://127.0.0.1:5000/page/1
# PUT       curl -i -H "Content-Type: application/json" -X PUT -d '{"page":"home update"}' http://127.0.0.1:5000/page/1
@controller.route('/page/<int:id>', methods=['GET','PUT'])
@validate_json
def page_read_update_delete(id):

    if request.method == 'GET':
        record  = Page.query.get(id)
        payload = jsonify(record.serialize(), result="OK") if record else jsonify([])
        return payload

    if request.method == 'PUT':
        record = Page.query.get(id)
        record.page = request.json['page']
        db.session.commit()
        payload = jsonify(record.serialize(), result="OK") if record else jsonify([])
        return payload


