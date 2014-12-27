from marshmallow import Schema
from marshmallow import ValidationError
from marshmallow import fields
from tektonik.models.page import Page as PageModel
from tektonik.models.path_page import PathPage as PathPageModel
from tektonik.models import db


class Page(Schema):

    """ Page schema """

    id = fields.Integer()
    page = fields.String()
    paths = fields.Method('get_paths')

    def get_paths(self, obj):
        page = db.aliased(PageModel)
        paths = PathPageModel.query. \
            join(page, PageModel). \
            filter(PathPageModel.page_id == obj.id). \
            filter(page.id == obj.id)

        result = list()
        for p in paths:
            result.append({
                'id': p.path.id,
                'path': p.path.path
            })

        return result

page_schema = Page()
page_schema_list = Page(many=True, only=('id', 'page', 'paths'))
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
