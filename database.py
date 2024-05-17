# Lucas Mathews - Fontys Student ID: 5023572
# Banking System Manager File

import os.path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#Import Config
from config import CONFIG 

# Check if the database exists
if os.path.exists(CONFIG["database"]["name"]):
    print(f"Database {CONFIG["database"]["name"]} already exists.")
else:
    print(f"Database {CONFIG["database"]["name"]} does not exist. Creating it now.")   

# Sets the database file to be used from the configuration file
db_url : str = "sqlite:///" + CONFIG["database"]["name"] 
print(f"Database file set to: {db_url}")    

# Creates the database engine (does not create the database file if it already exists)
engine = create_engine(db_url, echo=True)

#Import Classes
from class_base import Base # Imports the base class required by SQLAlchemy
from class_client import Client
from class_account import Account
from class_transaction import Transaction

# Create the tables in the database
Base.metadata.create_all(bind=engine) # Creates the tables in the database from the classes

# Creates a session to interact with the database
Session = sessionmaker(bind=engine) # Creates a session to interact with the database
session = Session() # Creates a session object
