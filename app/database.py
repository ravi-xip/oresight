from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import scoped_session, sessionmaker
import os

from config.settings import SQLALCHEMY_DATABASE_URI

current_env = os.environ.get('ENV', 'dev')
# Global engine and session factory

db: SQLAlchemy = SQLAlchemy()
if current_env == 'dev':
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={'check_same_thread': False}, poolclass=StaticPool)
Session = scoped_session(sessionmaker(bind=engine))


def get_db_session() -> scoped_session:
    return Session()
