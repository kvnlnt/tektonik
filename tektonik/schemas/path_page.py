from marshmallow import Schema
from marshmallow import fields
from tektonik.schemas.page import page_schema


class PathPage(Schema):

    """ Path schema """

    id = fields.Integer()
    page = fields.Nested(page_schema)

path_page_schema = PathPage
path_page_schema_list = PathPage(many=True, only=['page'])
