"""
:synopsis: Properties controller
"""

from flask import Blueprint
from flask import jsonify
from flask import request
from tektonik.models import db
from tektonik.models.page import Page as PageModel
from tektonik.schemas.page import page_schema
from tektonik.schemas.page import page_schema_read
from tektonik.schemas.page import page_schema_list
from tektonik.schemas.page import page_schema_search

blueprint = Blueprint('pages', __name__)


@blueprint.route("", methods=['GET'])
def list_pages():

    """ list pages """

    pages = PageModel.query.all()
    result, errors = page_schema_list.dump(pages)

    if errors:
        return jsonify({"result": errors}), 404
    else:
        return jsonify({"result": result}), 200


@blueprint.route("/search/<string:term>", methods=['GET'])
def search_pages(term=''):

    """ search for a page """

    records = PageModel.query. \
        filter(PageModel.page.like("%" + term + "%")).all()
    result, errors = page_schema_search.dump(records)

    if errors:
        return jsonify({"result": errors}), 404
    else:
        return jsonify({"result": result}), 200


@blueprint.route("", methods=['POST'])
def create_page():

    """ create new page """

    result, errors = page_schema.load(request.json)

    if errors:
        return jsonify({"errors": errors}), 403
    else:
        record = PageModel(page=result['page'])
        db.session.add(record)
        db.session.commit()
        record = page_schema.dump(record).data
        return jsonify(
            {"result":
                {"record": record,
                 "message": "Page successfully added"}}), 201


@blueprint.route("/<int:id>", methods=['GET'])
def read_page(id):

    """ get page details """

    record = PageModel.query.get(id)
    result, errors = page_schema_read.dump(record)

    if not record:
        return jsonify({"result": "Record not found"}), 404
    else:
        return jsonify({"result": result}), 200


@blueprint.route("/<int:id>", methods=['PUT', 'PATCH'])
def update_page(id):

    """ update page """

    record = PageModel.query.get(id)
    request.json['id'] = id
    result, errors = page_schema.load(request.json)

    if errors:
        return jsonify({"errors": errors}), 403
    else:
        record.page = result['page']
        db.session.commit()
        record = page_schema.dump(record).data
        return jsonify({"result": record}), 200


@blueprint.route("/<int:id>", methods=['DELETE'])
def delete_page(id):

    """ delete page """

    record = PageModel.query.get(id)
    result, errors = page_schema.dump(record)

    if not record:
        return jsonify({"result": "Record not found"}), 403
    else:
        db.session.delete(record)
        db.session.commit()
        return jsonify({"result": result}), 200
