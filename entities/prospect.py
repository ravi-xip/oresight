import uuid
from datetime import datetime
from typing import Optional

from app.database import db


class Prospect(db.Model):
    __tablename__ = 'prospects' # noqa

    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    url = db.Column(db.String(500), nullable=False)

    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    interest = db.Column(db.String(500), nullable=True)
    website_id = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, server_default='now()', onupdate='now()', nullable=False)

    def __init__(self,
                 name: Optional[str] = '',
                 category: Optional[str] = '',
                 email: Optional[str] = '',
                 phone: Optional[str] = '',
                 bio: Optional[str] = '',
                 interest: Optional[str] = '',
                 url: Optional[str] = '',
                 website_id: Optional[str] = ''):
        self.id = uuid.uuid4().hex
        self.name = name
        self.category = category
        self.email = email
        self.phone = phone
        self.bio = bio
        self.interest = interest
        self.url = url
        self.website_id = website_id
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def __repr__(self):
        return '<Prospect %r>' % self.name

    def to_dict(self):
        self_dict = {}
        for column in self.__table__.columns:
            self_dict[column.name] = getattr(self, column.name)
        return self_dict

    def __str__(self):
        return self.to_dict()
