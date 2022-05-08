import os

PROJECT_NAME = "OlympicMedalsApp"
VERSION = "0.0.1"
BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API_PREFIX = "/api/v1"
SQLALCHEMY_DATABASE_URL: str = os.getenv(
    "DATABASE_URI", f"sqlite:///{BASE_DIR}/sql_app.db"
)
POSTGRESQL_DATABASE_URL: str = "postgresql://user:password@postgresserver/db"
DEBUG = True
