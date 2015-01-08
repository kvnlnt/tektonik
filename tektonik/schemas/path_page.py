from marshmallow import fields
from marshmallow import Schema
from marshmallow import ValidationError
from tektonik.models.path_page import PathPage as PathPageModel
from tektonik.models.page import Page as PageModel


class PathPage(Schema):

    """ Path schema """

    id = fields.Integer()
    path_id = fields.Integer()
    page_id = fields.Integer()


path_page_schema = PathPage()


@PathPage.validator
def validate_path_page_exists(schema, input_data):

    path_id = input_data.get('path_id', None)
    page_id = input_data.get('page_id', None)
    page = PageModel.query.get(page_id)

    if path_id is None:
        raise ValidationError('Path is required', 'path_id')

    if not page:
        raise ValidationError('Page not found', 'page_id')


@PathPage.validator
def validate_path_page_unique(schema, input_data):

    # look for property with this name
    record_exists = PathPageModel.query.filter_by(
        path_id=input_data['path_id'],
        page_id=input_data['page_id']).first()

    # if exists, let's check it out
    if record_exists:
        raise ValidationError(
            'Page already belongs to path', 'page_id')
