from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app.models import Base
from app.settings import POSTGRESQL_DATABASE_URL, SQLALCHEMY_DATABASE_URL

postgresql_engine = create_engine(
    POSTGRESQL_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=postgresql_engine)
Base.metadata.create_all(bind=postgresql_engine)


sqlalchemy_engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=sqlalchemy_engine)
)
