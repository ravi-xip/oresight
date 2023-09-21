from typing import List, Type

from sqlalchemy.orm import scoped_session

from entities.prospect import Prospect


class ProspectRepository:
    def __init__(self, session: scoped_session = None):
        if session is None:
            raise Exception("Session is not provided")
        self.session = session

    def find_by_id(self, prospect_id: str):
        # Check if the prospect exists
        prospect = self.session.query(Prospect).filter(Prospect.id == prospect_id).first()
        if prospect is None:
            raise Exception("Prospect not found")
        return prospect

    def add(self, prospect: Prospect) -> Prospect:
        self.session.add(prospect)
        self.session.commit()
        return prospect

    def find_all(self):
        return self.session.query(Prospect).all()

    def find_by_website_id(self, website_id: str):
        return self.session.query(Prospect).filter(Prospect.website_id == website_id).all()
