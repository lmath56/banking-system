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

# Add sample data if enabled in the configuration file if the database is empty
if CONFIG["database"]["add_sample_data"] == "True": # Checks if sample data addition is enabled
    if session.query(Client).count() == 0: # Checks if the database is empty
        print(f"Sample data addition is disabled because the database is not empty.")
        print(f"Adding sample data to new database file {CONFIG["database"]["name"]}.")
        session.add(Client("f9a16945-b570-4153-ba63-413f2cc2768a", "Lucas Mathews", "24/08/1998", "17/04/2024", "Rachelsmolen 1, 5612MA, Eindhoven", "0612345678", "522499@student.fontys.nl", "7835062ec36ed529fe22cc63baf3ec18d347dacb21c9801da8ba0848cc18efdf1e51717dd5b1240f7556aca3947aa0722452858be6002c1d46b1f1c311b0e9d8", "Notes", True, True, "1, 2"))
        session.add(Client("5be2a74d-d55c-4de6-85a1-2ed6a355f2cd", "Rigby", "16/03/2018", "06/05/2024", "Rachelsmolen 1, 5612MA, Eindhoven", "0612345678", "522499@cat.fontys.nl", "d3e7df3c78682fbb51e8c6110b3926349bb426bc9834c640cd666519901aef3dfab7822d66fb2dd9e39eb5a8492f6801c2e17ba4c16b8fbcd159c036fe27d8bd", "Is a cat", True, False, "3"))
        session.add(Account("4c227b02-348c-4611-99a2-8967680cdee6", "Savings Account", "17/04/2024", "Savings", 3000, True, "Savings account", "1"))
        session.add(Account("b9d9b801-eaab-45be-a4d1-1f7b0bbf798f", "Spending Account", "17/04/2024", "Spending", 150, True, "Spending account", "1"))
        session.add(Account("f182f186-0a88-4f98-8a02-3a568c65aba7", "Cat Account", "06/05/2024", "Cat Account", 497, True, "Food savings", "2"))
        session.add(Transaction("9d989788-f983-4590-8de2-9aa0c8bec7d2", "Deposit", 5000, "17/04/2024", "Initial Deposit", 1, "23542335"))
        session.add(Transaction("153cee93-51c7-4114-b9ef-e307fbf0bf87", "Deposit", 100, "17/04/2024", "Initial Deposit", 2, "23542335"))
        session.add(Transaction("4bec761a-0f36-452f-a48a-127dcf526e47", "Deposit", 500, "06/05/2024", "Initial Deposit", 3, "23542335"))
        session.add(Transaction("227a2a9e-a13b-484b-b037-78deeeb0258c", "Withdrawal", 2000, "06/05/2024", "Uni Fees", 3, "Fontys University"))
        session.add(Transaction("7248a706-29a8-478b-a674-c12ebf9a904a", "Withdrawal", 50, "06/05/2024", "Groceries", 3, "Aldi"))
        session.add(Transaction("ba367c28-41e6-4f8a-9bfa-3819f7b89a58", "Withdrawal", 3, "06/05/2024", "Treats", 3, "ZooPlus"))
        session.commit()
    else:
        print(f"The database is not empty, skipping sample data addition.")
else:
    print(f"Sample data addition is disabled.")