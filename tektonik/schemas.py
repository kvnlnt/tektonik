from marshmallow import Schema
from marshmallow import ValidationError
from marshmallow import fields


class Property(Schema):
    property = fields.String(required=True)


@Property.error_handler
def handle_errors(schema, errors, obj):
    return errors


@Property.validator
def validate_property(schema, input_data):
    if 'property' in input_data:
        if input_data['property'] == "":
            raise ValidationError('error A', 'property')


@Property.validator
def validate_property_2(schema, input_data):
    if 'property' in input_data:
        if input_data['property'] == "":
            raise ValidationError('error B', 'property')
