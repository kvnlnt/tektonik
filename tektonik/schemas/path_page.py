import arrow
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
    is_persistent = fields.Boolean(default=True)
    effective_date = fields.DateTime(default=arrow.utcnow().isoformat())
    expiration_date = fields.DateTime(
        default=arrow.utcnow().replace(years=+100).isoformat())


path_page_schema = PathPage()
path_page_schema_list = PathPage(
    many=True, only=('id', 'path_id', 'page_id', 'is_persistent',
                     'effective_date', 'expiration_date'))


@PathPage.data_handler
def serialize_effective_date(serializer, records, instances):
    for record in records:
        record['effective_date'] = arrow.get(
            record['effective_date']).humanize()
        record['expiration_date'] = arrow.get(
            record['expiration_date']).humanize()
    return records


@PathPage.validator
def validate_path_page_exists(schema, input_data):

    path_id = input_data.get('path_id', None)
    page_id = input_data.get('page_id', None)

    if page_id is None or page_id == '':
        page = None
    else:
        page = PageModel.query.get(page_id)

    if path_id is None:
        raise ValidationError('Path is required', 'path_id')

    if page is None:
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
