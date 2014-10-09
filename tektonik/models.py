from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Property(db.Model):

    __tablename__ = 'properties'
    id = db.Column(db.Integer, primary_key=True)
    property = db.Column(db.String(100))


class Path(db.Model):

    __tablename__ = 'paths'
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(100))
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'))


class PathPage(db.Model):

    __tablename__ = 'path_pages'
    id = db.Column(db.Integer, primary_key=True)
    path_id = db.Column(db.Integer, db.ForeignKey('paths.id'))
    page_id = db.Column(db.Integer, db.ForeignKey('pages.id'))
    effective_date = db.Column(db.DateTime)
    expiration_date = db.Column(db.DateTime)


class Page(db.Model):

    __tablename__ = 'pages'
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.String(100))
