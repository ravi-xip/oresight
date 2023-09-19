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
        return self.session.query(Website).all()
