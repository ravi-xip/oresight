import uuid

from sqlalchemy import func

from app.database import db


class Website(db.Model):
    __tablename__ = 'websites'  # noqa

    id = db.Column(db.String(500), primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    url_filter = db.Column(db.String(500), nullable=False, default='')
    max_links = db.Column(db.Integer, nullable=False, default=100)
    num_prospects = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.String(500), nullable=False, default='PROCESSING')
    created_at = db.Column(db.TIMESTAMP, server_default='now()', nullable=False)
    updated_at = db.Column(db.TIMESTAMP, server_default='now()', onupdate='now()', nullable=False)

    def __init__(self,
                 name: str,
                 url: str,
                 max_links: int = 100,
                 url_filter: str = ''):
        self.id = uuid.uuid4().hex
        self.name = name
        self.url = url
        self.max_links = max_links
        self.url_filter = url_filter
        self.created_at = func.now()
        self.updated_at = func.now()

    def to_dict(self):
        self_dict = {}
        for column in self.__table__.columns:
            self_dict[column.name] = getattr(self, column.name)
        return self_dict
