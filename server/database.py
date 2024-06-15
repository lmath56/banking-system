# Lucas Mathews - Fontys Student ID: 5023572
# Banking System Manager File

from config import CONFIG # Import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_type = CONFIG.get('database', 'type')
db_user = CONFIG.get('database', 'user')
db_password = CONFIG.get('database', 'password')
db_ip = CONFIG.get('database', 'ip')
db_port = CONFIG.get('database', 'port')
db_name = CONFIG.get('database', 'name')

db_url : str = f"{db_type}://{db_user}:{db_password}@{db_ip}:{db_port}/{db_name}"

engine = create_engine(db_url, echo=True) # Creates the database engine

from class_base import Base # Imports the base class required by SQLAlchemy

Base.metadata.create_all(bind=engine) # Creates the tables in the database from the classes

Session = sessionmaker(bind=engine) # Creates a session to interact with the database
session = Session() # Creates a session object