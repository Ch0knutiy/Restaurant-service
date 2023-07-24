from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from models.models import Base

engine = create_engine("postgresql+psycopg2://postgres:root@localhost/Y_lab")
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
