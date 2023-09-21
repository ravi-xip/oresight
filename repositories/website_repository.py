from typing import Type

from sqlalchemy.orm import scoped_session

from entities.website import Website


class WebsiteRepository:
    def __init__(self, session: scoped_session = None):
        if session is None:
            raise Exception("Session is not provided")
        self.session = session

    def add(self, website: Website) -> Website:
        self.session.add(website)
        self.session.commit()
        return website

    def find_all(self):
        # Check if the session is valid
        if self.session is None:
            raise Exception("Session is not provided")
        return self.session.query(Website).all()

    def find_by_id(self, website_id: str):
        # Check if the session is valid
        if self.session is None:
            raise Exception("Session is not provided")
        return self.session.query(Website).filter_by(id=website_id).first()

    def update(self, website: Website) -> Website:
        # Validation check
        if not website.id or not website.name or not website.url:
            raise ValueError("Website's id, name, or url cannot be empty")

        # Number of prospects check (should be >=0)
        if website.num_prospects < 0:
            raise ValueError("Number of prospects cannot be negative")

        # Check on status (should be one of PROCESSING, INDEXING, COMPLETED, FAILED)
        if website.status not in ['PROCESSING', 'INDEXING', 'COMPLETED', 'FAILED']:
            raise ValueError("Status should be one of PROCESSING, INDEXING, COMPLETED, FAILED")

        # Existence check
        existing_website = self.session.query(Website).filter_by(id=website.id).first()
        if not existing_website:
            raise ValueError(f"Website with id {website.id} does not exist")

        self.session.merge(website)
        self.session.commit()
        return website
