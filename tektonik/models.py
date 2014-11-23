from flask.ext.sqlalchemy import SQLAlchemy

# create instance of sqlalchemy
db = SQLAlchemy()


class Property(db.Model):

    """ Property model. """

    __tablename__ = 'properties'
    id = db.Column(db.Integer, primary_key=True)
    property = db.Column(db.String(100))
    paths = db.relationship('Path', backref=db.backref('properties'))


class PathPage(db.Model):

    """ Path to Page model. """

    __tablename__ = 'path_pages'
    id = db.Column(db.Integer, primary_key=True)
    path_id = db.Column(db.Integer, db.ForeignKey('paths.id'))
    page_id = db.Column(db.Integer, db.ForeignKey('pages.id'))
    effective_date = db.Column(db.DateTime)
    expiration_date = db.Column(db.DateTime)
    page = db.relationship("Page", backref="path_page")


class Path(db.Model):

    """ Path model """

    __tablename__ = 'paths'
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(100))
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'))
    pages = db.relationship(
        'PathPage',
        backref='path',
        cascade="save-update, merge, delete, delete-orphan"
    )


class Page(db.Model):

    """ Page model """

    __tablename__ = 'pages'
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.String(100))
