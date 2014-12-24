from tektonik.types import LowerCaseText
from tektonik.models import db


class Page(db.Model):

    """ Page model """

    __tablename__ = 'pages'
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(LowerCaseText(100))
