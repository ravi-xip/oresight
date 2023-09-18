from sqlalchemy import func

from app.database import db


class Website(db.Model):
    __tablename__ = 'websites'

    id = db.Column(db.String(500), primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default='now()', nullable=False)
    updated_at = db.Column(db.TIMESTAMP, server_default='now()', onupdate='now()', nullable=False)

    def __init__(self,
                 id: str,
                 name: str,
                 url: str):
        self.id = id
        self.name = name
        self.url = url
        self.created_at = func.now()
        self.updated_at = func.now()

    def to_dict(self):
        self_dict = {}
        for column in self.__table__.columns:
            self_dict[column.name] = getattr(self, column.name)
        return self_dict
