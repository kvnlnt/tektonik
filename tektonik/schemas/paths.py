from marshmallow import Schema
from marshmallow import fields
from marshmallow import ValidationError
from tektonik.models import Path as PathModel


class Path(Schema):

    """ Path schema """

    # validations
    def min(value, error=None):
        if len(value) == 0:
            raise ValidationError("Path is required")

        if len(value) < 3:
            raise ValidationError("Path too short (< 3)", 'property')

    def max(value, error=None):
        if len(value) > 100:
            raise ValidationError("Path too long (> 100)", 'property')

    # fields
    id = fields.Integer()
    path = fields.String(
        required=True,
        validate=[min, max]
    )

    # json fields
    class Meta:
        fields = ('id', 'path')


@Path.validator
def validate_unique_path(schema, input_data):

    # look for property with this name
    record_exists = PathModel.query.filter_by(
        path=input_data['path']).first()

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
            raise ValidationError('Path already exists', 'property')

        if is_new:
            raise ValidationError('Path already exists', 'property')
