from tektonik.types import LowerCaseText
from tektonik.models import db


class Property(db.Model):

    """ Property model. """

    __tablename__ = 'properties'
    id = db.Column(db.Integer, primary_key=True)
    property = db.Column(LowerCaseText(100), unique=True)

    def list_stats(self):

        sql = """
            SELECT
                    count(distinct page.id) as total_pages,
                    count(distinct path.id) as total_paths
            FROM
                    properties as property,
                    paths as path,
                    path_pages as path_page,
                    pages as page
             WHERE
                    property.id = :id AND
                    path.property_id = property.id AND
                    path_page.path_id = path.id AND
                    path_page.page_id = page.id
            """

        query = db.engine.execute(sql, id=self.id)
        stats = query.fetchone()

        result = {
            'total_paths': stats.total_paths,
            'total_pages': stats.total_pages
        }

        return result
