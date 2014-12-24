from marshmallow import Schema
from marshmallow import fields
from marshmallow import ValidationError
from tektonik.models.property import Property as PropertyModel


class Property(Schema):

    """ Property schema """

    # fields
    id = fields.Integer()
    property = fields.String()

    # json fields
    class Meta:
        fields = ('id', 'property')


@Property.validator
def validate_property_min(schema, input_data):

    if len(input_data['property']) == 0:
        raise ValidationError('Property is required', 'property')

    if len(input_data['property']) > 0 and len(input_data['property']) < 3:
        raise ValidationError(
            'Property be at least three characters long', 'property')


@Property.validator
def validate_property_max(schema, input_data):

    if len(input_data['property']) > 100:
        raise ValidationError('Property too long (> 100)', 'property')


@Property.validator
def validate_unique_property(schema, input_data):

    # look for property with this name
    record_exists = PropertyModel.query.filter_by(
        property=input_data['property']).first()

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
            raise ValidationError('Property already exists', 'property')

        if is_new:
            raise ValidationError('Property already exists', 'property')
