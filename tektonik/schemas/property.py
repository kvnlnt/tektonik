from marshmallow import Schema
from marshmallow import fields
from marshmallow import ValidationError
from tektonik.models.property import Property as PropertyModel
from tektonik.models import db


class Property(Schema):

    """ Property schema """

    # fields
    id = fields.Integer()
    property = fields.String()
    stats = fields.Method('get_stats')

    def get_stats(self, obj):

        stats_sql = """
            SELECT
                    count(distinct page.id) as total_pages,
                    count(distinct path.id) as total_paths
            FROM
                    properties as property,
                    paths as path,
                    path_pages as path_page,
                    pages as page
             WHERE
                    property.id = :id AND
                    path.property_id = property.id AND
                    path_page.path_id = path.id AND
                    path_page.page_id = page.id
            """

        stats_query = db.engine.execute(stats_sql, id=obj.id)
        stats_data = stats_query.fetchone()

        result = {
            'total_paths': stats_data.total_paths,
            'total_pages': stats_data.total_pages
        }

        return result

    # json fields
    class Meta:
        fields = ('id', 'property')


property_schema = Property()
property_schema_read = Property(
    only=('id', 'property', 'stats')
)
property_schema_list = Property(
    many=True,
    only=('id', 'property', 'stats')
)


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
