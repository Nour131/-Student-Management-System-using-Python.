
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./students.db"


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def get_db():
    """
    Dependency used by FastAPI routes.
    Opens a session, hands it to the route, then always closes it
    afterwards (even if the route raises an error).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
