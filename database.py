from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create the engine that will interact with the database
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create a base class to define models
Base = declarative_base()

# Create a session local class for database interaction
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
