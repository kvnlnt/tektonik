from tektonik.types import LowerCaseText
from tektonik.models import db


class Path(db.Model):

    """ Path model """

    __tablename__ = 'paths'
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(LowerCaseText(100))
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'))

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
        rows = query.fetchall()

        result = list()
        for row in rows:
            result.append({
                'id': row.id,
                'page': row.page
            })

        return result
