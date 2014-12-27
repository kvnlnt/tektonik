from tektonik.types import LowerCaseText
from tektonik.models import db


class Property(db.Model):

    """ Property model. """

    __tablename__ = 'properties'
    id = db.Column(db.Integer, primary_key=True)
    property = db.Column(LowerCaseText(100), unique=True)
