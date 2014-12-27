from tektonik.types import LowerCaseText
from tektonik.models import db


class Path(db.Model):

    """ Path model """

    __tablename__ = 'paths'
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(LowerCaseText(100))
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'))

    def get_property(self):

        sql = """
                SELECT
                    property.id,
                    property.property
                FROM
                    properties as property
                WHERE
                    property.id = :id
            """

        query = db.engine.execute(sql, id=self.property_id)
        record = query.fetchone()

        result = {
            'id': record.id,
            'property': record.property
        }

        return result

    def list_pages(self):

        sql = """
                SELECT
                        page.id,
                        page.page
                FROM
                        path_pages as path_page,
                        pages as page
                WHERE
                        path_page.path_id = :id AND
                        path_page.page_id = page.id
            """

        query = db.engine.execute(sql, id=self.id)
        records = query.fetchall()

        result = list()
        for row in records:
            result.append({
                'id': row.id,
                'page': row.page
            })

        return result
