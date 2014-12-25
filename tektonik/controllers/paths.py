"""
:synopsis: Properties controller
"""

from flask import Blueprint
from flask import jsonify
from flask import request
from tektonik.models import db
from tektonik.models.path import Path as PathModel
from tektonik.schemas.path import path_schema
from tektonik.schemas.path import path_schema_list
from tektonik.schemas.path import path_schema_read

blueprint = Blueprint('paths', __name__)


@blueprint.route("", methods=['GET'])
def list_paths():

    paths = PathModel.query.all()
    result, errors = path_schema_list.dump(paths)

    if errors:
        return jsonify({"result": errors}), 404
    else:
        return jsonify({"result": result}), 200


@blueprint.route("", methods=['POST'])
def create_path():
    """ create new path """

    result, errors = path_schema.load(request.json)

    if errors:
        return jsonify({"errors": errors}), 403
    else:
        record = PathModel(
            path=result['path'],
            property_id=result['property_id'])
        db.session.add(record)
        db.session.commit()
        record = path_schema.dump(record).data
        return jsonify(
            {"result":
                {"record": record,
                 "message": "Path successfully added"}}), 201


@blueprint.route("/<int:id>", methods=['GET'])
def read_path(id):

    record = PathModel.query.get(id)
    result, errors = path_schema_read.dump(record)

    if not record:
        return jsonify({"result": "Record not found"}), 404
    else:
        return jsonify({"result": result}), 200


@blueprint.route("/<int:id>", methods=['PUT', 'PATCH'])
def update_path(id):

    record = PathModel.query.get(id)
    result, errors = path_schema.load(request.json)

    if errors:
        return jsonify({"errors": errors}), 403
    else:
        record.path = result['path']
        db.session.commit()
        record = path_schema.dump(record).data
        return jsonify({"result": record}), 200


@blueprint.route("/<int:id>", methods=['DELETE'])
def delete_path(id):

    record = PathModel.query.get(id)
    result, errors = path_schema.dump(record)

    if not record:
        return jsonify({"result": "Record not found"}), 403
    else:
        db.session.delete(record)
        db.session.commit()
        return jsonify({"result": result}), 200
