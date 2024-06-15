# Lucas Mathews - Fontys Student ID: 5023572
# Banking System Databas File

from config import CONFIG # Import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import time
from logger import event_logger

db_type = CONFIG.get('database', 'type')
db_user = CONFIG.get('database', 'user')
db_password = CONFIG.get('database', 'password')
db_ip = CONFIG.get('database', 'ip')
db_port = CONFIG.get('database', 'port')
db_name = CONFIG.get('database', 'name')

db_url : str = f"{db_type}://{db_user}:{db_password}@{db_ip}:{db_port}/{db_name}"

try: # Retry connecting to the database with a retry mechanism
    max_retries = 10
    retries = 0
    engine = None
    while retries < max_retries:
        try:
            engine = create_engine(db_url, echo=True)
            break
        except OperationalError as e:
            event_logger(f"Failed to connect to database: {e}")
            retries += 1
            event_logger(f"Retrying ({retries}/{max_retries})...")
            time.sleep(10)  # Wait 10 seconds before retrying

    if engine:
        from class_base import Base # Imports the base class required by SQLAlchemy
        Base.metadata.create_all(bind=engine) # Creates the tables in the database from the classes
        Session = sessionmaker(bind=engine) # Creates a session to interact with the database
        session = Session() # Creates a session object

except Exception as e:
    event_logger(f"Error: {e}")

finally:
    if 'session' in locals():
        session.close()  # Close the session when done

event_logger("Database operations completed.")