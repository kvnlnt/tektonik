from marshmallow import Schema
from marshmallow import ValidationError
from marshmallow import fields


class Property(Schema):

    # validations
    def property_min_length(value, error=None):
        if len(value) < 3:
            raise ValidationError("Property too short (< 3)", 'property')

    def property_max_length(value, error=None):
        if len(value) > 100:
            raise ValidationError("Propert too long (> 100)", 'property')

    # fields
    id = fields.Integer()
    property = fields.String(
        required=True,
        validate=[property_min_length, property_max_length]
    )

    # json fields
    class Meta:
        fields = ('id', 'property')
