from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Portfolio(Base):
    __tablename__ = "portfolio"

    id = Column(Integer, primary_key=True)
    ime = Column(String(120), nullable=False)
    prezime = Column(String(120), nullable=False)
    godini = Column(Integer, nullable=False)
    kratko_bio = Column(Text(120), nullable=True)
    nasoka = Column(String(120), nullable=False)
    vestini = Column(String(120), nullable=True)
    proekti_iskustva = Column(String(120), nullable=True)
