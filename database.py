from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model_database import Base

engine = create_engine("sqlite:///app.db")
SessionLocal = sessionmaker(bind=engine)

session = SessionLocal()

Base.metadata.create_all(bind=engine)

