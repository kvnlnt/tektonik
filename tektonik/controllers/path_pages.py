"""
:synopsis: Properties controller
"""

from flask import Blueprint
from flask import jsonify
from flask import request
from tektonik.models import db
from tektonik.models.path_page import PathPage as PathPageModel
from tektonik.schemas.path_page import path_page_schema, path_page_schema_list

blueprint = Blueprint('path_pages', __name__)


@blueprint.route("", methods=['POST'])
def create_path_page():

    """ create new path """

    result, errors = path_page_schema.load(request.json)

    if errors:
        return jsonify({"errors": errors}), 403
    else:
        record = PathPageModel(
            path_id=result['path_id'],
            page_id=result['page_id'],
            is_persistent=result['is_persistent'],
            effective_date=result['effective_date'],
            expiration_date=result['expiration_date'])
        db.session.add(record)
        db.session.commit()
        record = path_page_schema.dump(record).data
        return jsonify(
            {"result":
                {"record": record,
                 "message": "Page successfully added"}}), 201


@blueprint.route("", methods=['GET'])
def list_path_pages():

    """ list pages """

    path_pages = PathPageModel.query.all()
    result, errors = path_page_schema_list.dump(path_pages)
    metadata = {"total_records": PathPageModel.query.count()}

    if errors:
        return jsonify({"result": errors}), 404
    else:
        return jsonify({"result": result, "metadata": metadata}), 200


@blueprint.route("/<int:id>", methods=['DELETE'])
def delete_path_page(id):

    """ delete path """

    record = PathPageModel.query.get(id)
    result, errors = path_page_schema.dump(record)

    if not record:
        return jsonify({"result": "Record not found"}), 403
    else:
        db.session.delete(record)
        db.session.commit()
        return jsonify({"result": result}), 200
