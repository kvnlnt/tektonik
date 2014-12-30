from tektonik.types import LowerCaseText
from tektonik.models import db
from tektonik.models.path_page import PathPage as PathPageModel


class Path(db.Model):

    """ Path model """

    __tablename__ = 'paths'
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(LowerCaseText(100))
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'))

    def add_pages(self, pages, reset=False):

        if reset:
            PathPageModel.query.filter(
                PathPageModel.path_id == self.id).delete()

        if pages:
            for page in pages:
                try:
                    # XXX
                    # really should verify if page exists before adding
                    new_page = PathPageModel(
                        path_id=self.id, page_id=page['id'])
                    db.session.add(new_page)
                except:
                    pass

            db.session.commit()

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
                        path_page.id as path_page_id,
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
                'page': row.page,
                'path_page_id': row.path_page_id
            })

        return result
