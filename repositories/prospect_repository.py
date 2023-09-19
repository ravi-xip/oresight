from sqlalchemy.orm import scoped_session

from entities.prospect import Prospect


class ProspectRepository:
    def __init__(self, session: scoped_session = None):
        if session is None:
            raise Exception("Session is not provided")
        self.session = session

    def add(self, prospect: Prospect) -> Prospect:
        self.session.add(prospect)
        self.session.commit()
        return prospect

    def find_all(self):
        return self.session.query(Prospect).all()
