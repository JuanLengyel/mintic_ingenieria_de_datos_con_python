from sqlalchemy import Column, String, Integer

from base import Base

class Article(Base):
    __tablename__ = 'articles'

    id = Column(String, primary_key=True)
    body = Column(String)
    host = Column(String)
    title = Column(String)
    newspaper_uid = Column(String)
    n_token_body = Column(Integer)
    n_token_title = Column(Integer)
    url = Column(String, unique=True)

    def __init__ (self,
                  uid,
                  body,
                  host,
                  title,
                  newspaper_uid,
                  n_token_body,
                  n_token_title,
                  url):
        self.id = uid
        self.body = body
        self.host = host
        self.title = title
        self.newspaper_uid = newspaper_uid
        self.n_token_body = n_token_body
        self.n_token_title = n_token_title
        self.url = url