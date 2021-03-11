from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost/database_name"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:12345@localhost/blog_fastapi_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

sessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# mapping the connection
Base_db = declarative_base()