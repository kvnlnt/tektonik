"""
:synopsis: Properties controller
"""

from flask import Blueprint
from flask import jsonify
from flask import request
from tektonik.models import db
from tektonik.models import Page as PageModel
from tektonik.schemas.pages import Page as PageSchema

blueprint = Blueprint('pages', __name__)


@blueprint.route("", methods=['GET'])
def list_pages():

    pages = PageModel.query.all()
    schema = PageSchema(many=True)
    result, errors = schema.dump(pages)

    if errors:
        return jsonify({"result": errors}), 404
    else:
        return jsonify({"result": result}), 200


@blueprint.route("", methods=['POST'])
def create_page():
    """ create new page """

    schema = PageSchema()
    result, errors = schema.load(request.json)

    if errors:
        return jsonify({"errors": errors}), 403
    else:
        record = PageModel(page=result['page'])
        db.session.add(record)
        db.session.commit()
        record = schema.dump(record).data
        return jsonify(
            {"result":
                {"record": record,
                 "message": "Page successfully added"}}), 201


@blueprint.route("/<int:id>", methods=['GET'])
def read_page(id):

    record = PageModel.query.get(id)
    schema = PageSchema()
    result, errors = schema.dump(record)

    if not record:
        return jsonify({"result": "Record not found"}), 404
    else:
        return jsonify({"result": result}), 200


@blueprint.route("/<int:id>", methods=['PUT', 'PATCH'])
def update_page(id):

    record = PageModel.query.get(id)
    schema = PageSchema()
    result, errors = schema.load(request.json)

    if errors:
        return jsonify({"errors": errors}), 403
    else:
        record.page = result['page']
        db.session.commit()
        record = schema.dump(record).data
        return jsonify({"result": record}), 200


@blueprint.route("/<int:id>", methods=['DELETE'])
def delete_page(id):

    record = PageModel.query.get(id)
    schema = PageSchema()
    result, errors = schema.dump(record)

    if not record:
        return jsonify({"result": "Record not found"}), 403
    else:
        db.session.delete(record)
        db.session.commit()
        return jsonify({"result": result}), 200
