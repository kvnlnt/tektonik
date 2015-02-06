from tektonik.models import db


class PathPage(db.Model):

    """ Path to Page model. """

    __tablename__ = 'path_pages'
    id = db.Column(db.Integer, primary_key=True)
    path_id = db.Column(db.Integer, db.ForeignKey('paths.id'))
    page_id = db.Column(db.Integer, db.ForeignKey('pages.id'))
    is_persistent = db.Column(db.Boolean, default=1)
    effective_date = db.Column(db.DateTime)
    expiration_date = db.Column(db.DateTime)
