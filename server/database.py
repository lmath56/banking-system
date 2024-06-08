# Lucas Mathews - Fontys Student ID: 5023572
# Banking System Manager File

from config import CONFIG # Import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url : str = f"{CONFIG['database']['type']}://{CONFIG['database']['user']}:{CONFIG['database']['password']}@{CONFIG['database']['ip']}:{CONFIG['database']['port']}/{CONFIG['database']['name']}"
print(f"Database URL set to: {db_url}")    

engine = create_engine(db_url, echo=True) # Creates the database engine

from class_base import Base # Imports the base class required by SQLAlchemy

Base.metadata.create_all(bind=engine) # Creates the tables in the database from the classes

Session = sessionmaker(bind=engine) # Creates a session to interact with the database
session = Session() # Creates a session object