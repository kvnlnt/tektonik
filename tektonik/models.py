from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Property(db.Model):

    __tablename__ = 'properties'
    id = db.Column(db.Integer, primary_key=True)
    property = db.Column(db.String(100))

    def serialize(self):
        return {
            'id': self.id,
            'property' : self.property
        }


class Path(db.Model):

    __tablename__ = 'paths'
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(100))
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'))

    def serialize(self):
        return {
            'id': self.id,
            'path' : self.path,
            'property_id' : self.property_id
        }

class Page(db.Model):

    __tablename__ = 'pages'
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.String(100))

    def serialize(self):
        return {
            'id': self.id,
            'page' : self.page
        }
