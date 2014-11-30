from marshmallow import Schema
from marshmallow import fields
from marshmallow import ValidationError
from tektonik.models import Property as PropertyModel


class Property(Schema):

    """ Property schema """

    # validations
    def min(value, error=None):
        if len(value) < 3:
            raise ValidationError("Property too short (< 3)", 'property')

    def max(value, error=None):
        if len(value) > 100:
            raise ValidationError("Property too long (> 100)", 'property')

    def dup(value, error=None):
        record = PropertyModel.query.filter_by(property=value).first()
        if record:
            raise ValidationError("Property already exists")

    # fields
    id = fields.Integer()
    property = fields.String(
        required=True,
        validate=[min, max, dup]
    )

    # json fields
    class Meta:
        fields = ('id', 'property')
