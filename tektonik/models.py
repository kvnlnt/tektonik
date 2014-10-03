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

