# models.py
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///database.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Record(Base):
    __tablename__ = "records"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    date = Column(DateTime)
    explanation = Column(String)
    category = Column(String)
    email = Column(String)

Base.metadata.create_all(engine)