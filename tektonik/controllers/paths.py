"""
:synopsis: Properties controller
"""

from flask import Blueprint
from flask import jsonify
from flask import request
from tektonik.models import db
from tektonik.models.path import Path as PathModel
from tektonik.models.path_page import PathPage as PathPageModel
from tektonik.schemas.path import path_schema
from tektonik.schemas.path import path_schema_list
from tektonik.schemas.path import path_schema_read

blueprint = Blueprint('paths', __name__)


@blueprint.route("", methods=['GET'])
def list_paths():

    """ list paths """

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

    """ get path details """

    record = PathModel.query.get(id)
    result, errors = path_schema_read.dump(record)

    if not record:
        return jsonify({"result": "Record not found"}), 404
    else:
        return jsonify({"result": result}), 200


@blueprint.route("/<int:id>", methods=['PUT', 'PATCH'])
def update_path(id):

    """ update path """

    record = PathModel.query.get(id)
    request.json['id'] = id
    result, errors = path_schema.load(request.json)

    if errors:
        return jsonify({"errors": errors}), 403
    else:

        # if has pages, reset path_page configuration
        pages = request.json.get('pages', None)
        if pages:
            PathPageModel.query.filter(PathPageModel.path_id == id).delete()
            for page in pages:
                try:
                    # XXX
                    # one user could delete a page while another is
                    # adding is, thus causing this paths registration to
                    # this page to be orphaned
                    new_page = PathPageModel(path_id=id, page_id=page['id'])
                    db.session.add(new_page)
                except:
                    pass

        record.path = result['path']
        db.session.commit()
        record = path_schema.dump(PathModel.query.get(id)).data
        return jsonify({"result": record}), 200


@blueprint.route("/<int:id>", methods=['DELETE'])
def delete_path(id):

    """ delete path """

    record = PathModel.query.get(id)
    result, errors = path_schema.dump(record)

    if not record:
        return jsonify({"result": "Record not found"}), 403
    else:
        db.session.delete(record)
        db.session.commit()
        return jsonify({"result": result}), 200
