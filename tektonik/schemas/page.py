from marshmallow import Schema
from marshmallow import ValidationError
from marshmallow import fields
from tektonik.models.page import Page as PageModel


class Page(Schema):

    """ Page schema """

    id = fields.Integer()
    page = fields.String()
    paths = fields.Function(PageModel.list_paths)


page_schema = Page()
page_schema_list = Page(many=True, only=('id', 'page', 'paths'))
page_schema_search = Page(many=True, only=('id', 'page'))
page_schema_read = Page(only=('id', 'page', 'paths'))


@Page.validator
def validate_page_min(schema, input_data):

    if len(input_data['page']) == 0:
        raise ValidationError('Page is required', 'page')

    if len(input_data['page']) > 0 and len(input_data['page']) < 1:
        raise ValidationError(
            'Page be at least one characters long', 'page')


@Page.validator
def validate_page_max(schema, input_data):

    if len(input_data['page']) > 100:
        raise ValidationError('Page too long (> 100)', 'page')


@Page.validator
def validate_unique_property(schema, input_data):

    # look for property with this name
    record_exists = PageModel.query.filter_by(
        page=input_data['page']).first()

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
            raise ValidationError('Page already exists', 'page')

        if is_new:
            raise ValidationError('Page already exists', 'page')
