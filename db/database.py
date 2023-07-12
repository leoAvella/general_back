from sqlalchemy.exc import OperationalError
import logging
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()


# Add error handling for the case where the database connection cannot be established
engine = None
session_local = None

class DBConnection:
    def __init__(self):
        self.engine = None
        self.session_local = None

    def create_engine(self):
        try:
            db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
            self.engine = create_engine(db_url)
        except Exception as e:
            logging.exception(f"Failed to establish database connection: {str(e)}")
            return None

    def get_db_connection(self):
        if self.engine is None:
            self.create_engine()
        try:
            connection = self.engine.connect()
            self.session_local = sessionmaker(autocommit=False, autoflush=False, bind=connection)
            db = self.session_local()
            try:
                yield db
            except Exception as e:
                logging.exception(f"An error occurred: {str(e)}")
            finally:
                db.close()
        except (OperationalError, NameError, ArgumentError) as e:
            logging.exception(f"Failed to establish database connection: {str(e)}")

# Create the sessionmaker once and reuse it in subsequent calls to improve performance
engine = create_engine(f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}")
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)