from tektonik.types import LowerCaseText
from tektonik.models import db


class Path(db.Model):

    """ Path model """

    __tablename__ = 'paths'
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(LowerCaseText(100))
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'))
    pages = db.relationship(
        'PathPage',
        backref='path',
        cascade="save-update, merge, delete, delete-orphan"
    )
