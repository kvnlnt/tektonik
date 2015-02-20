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
    effective_date = fields.DateTime()
    expiration_date = fields.DateTime()


path_page_schema = PathPage()
path_page_schema_list = PathPage(
    many=True, only=('id', 'path_id', 'page_id', 'is_persistent',
                     'effective_date', 'expiration_date'))


@PathPage.data_handler
def serialize_effective_date(serializer, records, instances):

    if type(records) is dict:
        records = [records]

    for record in records:
        record['effective_date_humanized'] = arrow.get(
            record['effective_date']).humanize() \
            if record['effective_date'] else None
        record['expiration_date_humanized'] = arrow.get(
            record['expiration_date']).humanize() \
            if record['expiration_date'] else None
    return records


@PathPage.validator
def validate_path_id(schema, input_data):
    path_id = input_data.get('path_id', None)
    if path_id is None:
        raise ValidationError('Path is required', 'path_id')


@PathPage.validator
def validate_page_id(schema, input_data):
    page_id = input_data.get('page_id', None)
    if page_id is None:
        raise ValidationError('Page is required', 'page_id')


@PathPage.validator
def validate_path_page_exists(schema, input_data):

    path_id = input_data.get('path_id', None)
    page_id = input_data.get('page_id', 0)
    page = PageModel.query.get(page_id)

    if path_id is None or page is None:
        raise ValidationError('Page is required', 'page_id')


@PathPage.validator
def validate_path_page_unique(schema, input_data):

    path_id = input_data.get('path_id', None)
    page_id = input_data.get('page_id', '')

    # look for property with this name
    record_exists = PathPageModel.query.filter_by(
        path_id=path_id,
        page_id=page_id).first()

    # if exists, let's check it out
    if record_exists:
        raise ValidationError(
            'Page already belongs to path', 'page_id')


@PathPage.validator
def validate_effective_date(schema, input_data):
    # only need to check for none as it has a default
    effective_date = input_data.get('effective_date', None)
    if effective_date is None:
        raise ValidationError('Effective date is required', 'effective_date')


@PathPage.validator
def validate_expiration_date(schema, input_data):
    expiration_date = input_data.get('expiration_date', None)
    expiration_date = None if expiration_date == '' else expiration_date
    is_persistent = input_data.get('is_persistent', None)
    is_persistent = None if is_persistent == '' else is_persistent
    if expiration_date is None and is_persistent is None:
        raise ValidationError(
            'Expiration date or Show Forever must be specified',
            'expiration_date')


@PathPage.validator
def validate_is_persistent(schema, input_data):
    expiration_date = input_data.get('expiration_date', None)
    is_persistent = input_data.get('is_persistent', None)
    if expiration_date is None and is_persistent is None:
        raise ValidationError(
            'Show Forever or Expiration date or must be specified',
            'is_persistent')
