from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database connection URL
DATABASE_URL = os.getenv('DATABASE_URL')
# Create sqlalchemy database engine (establishes connection to the database)
engine = create_engine(DATABASE_URL)
# Declare new session maker (establishes all conversations with the database)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# All dataclasses should inherit from Base
Base = declarative_base()
