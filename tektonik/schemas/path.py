from marshmallow import fields
from marshmallow import Schema
from marshmallow import ValidationError
from tektonik.models.path import Path as PathModel
from tektonik.models.property import Property as PropertyModel


class Path(Schema):

    """ Path schema """

    id = fields.Integer()
    path = fields.String()
    property_id = fields.Integer()
    property = fields.Function(PathModel.get_property)
    pages = fields.Function(PathModel.list_pages)


path_schema = Path()
path_schema_list = Path(
    many=True, only=('id', 'path', 'property', 'pages'))
path_schema_read = Path(
    only=('id', 'path', 'property_id', 'property', 'pages'))


@Path.validator
def validate_path_min(schema, input_data):

    if len(input_data['path']) == 0:
        raise ValidationError('Path is required', 'path')

    if len(input_data['path']) > 0 and len(input_data['path']) < 3:
        raise ValidationError(
            'Path be at least three characters long', 'path')


@Path.validator
def validate_path_max(schema, input_data):

    if len(input_data['path']) > 100:
        raise ValidationError('Path too long (> 100)', 'path')


@Path.validator
def validate_path_exists(schema, input_data):

    property = PropertyModel.query.filter(
        PropertyModel.id == input_data['property_id'])
    if property.count() == 0:
        raise ValidationError('Property must be specified', 'property_id')


@Path.validator
def validate_path_unique(schema, input_data):

    # look for property with this name
    record_exists = PathModel.query.filter_by(
        path=input_data['path'],
        property_id=input_data['property_id']).first()

    # default an id for easier handling
    id = input_data.get('id', None)

    # if exists, let's check it out
    if record_exists:

        # is this an update
        is_update = True if id is not None else False

        # is new record
        is_new = not is_update

        # is the id the same as that passed in?
        is_id_same = record_exists.id == id

        # if this is an update and the id is different, it's a conflict
        if is_update is True and is_id_same is False:
            raise ValidationError(
                'Path already exists for selected property', 'path')

        if is_new:
            raise ValidationError(
                'Path already exists for selected property', 'path')
