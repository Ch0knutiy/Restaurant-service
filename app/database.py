from models.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql+psycopg2://postgres:root@postgres_y_lab/postgres')
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
