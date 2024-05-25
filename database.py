# Lucas Mathews - Fontys Student ID: 5023572
# Banking System Manager File

import os.path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import CONFIG # Import Config

if os.path.exists(CONFIG["database"]["name"]): # Check if the database exists
    print(f"Database {CONFIG["database"]["name"]} already exists.")
else:
    print(f"Database {CONFIG["database"]["name"]} does not exist. Creating it now.")   

db_url : str = "sqlite:///" + CONFIG["database"]["name"] # Sets the database file to be used from the configuration file
print(f"Database file set to: {db_url}")    

engine = create_engine(db_url, echo=True) # Creates the database engine (does not create the database file if it already exists)

from class_base import Base # Imports the base class required by SQLAlchemy

Base.metadata.create_all(bind=engine) # Creates the tables in the database from the classes

Session = sessionmaker(bind=engine) # Creates a session to interact with the database
session = Session() # Creates a session object
