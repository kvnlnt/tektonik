from tektonik.types import LowerCaseText
from tektonik.models import db


class Page(db.Model):

    """ Page model """

    __tablename__ = 'pages'
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(LowerCaseText(100), unique=True)

    def list_paths(self):

        sql = """
                SELECT
                        path.id,
                        path.path
                FROM
                        path_pages as path_page,
                        paths as path
                WHERE
                        path_page.page_id = :id AND
                        path_page.path_id = path.id
            """

        query = db.engine.execute(sql, id=self.id)
        rows = query.fetchall()

        result = list()
        for row in rows:
            result.append({
                'id': row.id,
                'path': row.path
            })

        return result
