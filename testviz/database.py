from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

Base = declarative_base()

def init_db(database_url):
  engine = create_engine(database_url, convert_unicode=True)
  global db_session
  db_session = scoped_session(sessionmaker(autocommit=False,
                                           autoflush=False,
                                           bind=engine))

  Base.query = db_session.query_property()

  import models
  Base.metadata.create_all(bind=engine)
