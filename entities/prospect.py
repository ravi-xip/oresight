from sqlalchemy import ForeignKey

from app.database import db


class Prospect(db.Model):
    __tablename__ = 'prospects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    website_id = db.Column(db.String(500), ForeignKey("websites.id"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, server_default='now()', onupdate='now()', nullable=False)

    def __repr__(self):
        return '<Prospect %r>' % self.name
