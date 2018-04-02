import enum

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Column, Date, Enum, Integer, String

# In SQLAlchemy, the ORM begins with a declarative base class.
# Both describes and maps classes to tables.
Base = declarative_base()

# Define settings for database.
# Supports postgres, mysql, sqlite - provisioning required for the first two
settings = {
    'DATABASE': {
        'URL': 'sqlite:///db.sqlite3',
        'METADATA': Base.metadata
    }
}

# Define 'models'
class BookModel(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(256))
    author = Column(String(256))
    publisher = Column(String(256))
    publish_date = Column(Date)
    rating = Column(Integer)
    checked_out = Column(Boolean, default=False)

    def __repr__(self):
        return('<Book(id=\'{0}\', title=\'{1}\')>'.format(self.id, self.title))
