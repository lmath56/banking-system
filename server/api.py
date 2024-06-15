# Lucas Mathews - Fontys Student ID: 5023572
# Banking System API

###############
### Modules ###
###############

import subprocess
import connexion # Imports connexion module
from config import CONFIG # Imports the configuration file
from manager import * # Imports the Manager file that contains the functions for the API
from flask_session import Session # Imports the session module 


#################
### Connexion ###
#################

def create_app():
    """Creates the API using Connexion."""
    app = connexion.FlaskApp(__name__)
    app.add_api(CONFIG["server"]["api_file"])
    flask_app = app.app
    flask_app.config['SECRET_KEY'] = CONFIG["sessions"]["secret_key"]
    flask_app.config['SESSION_TYPE'] = 'filesystem'
    Session(flask_app)
    event_logger("Session initialised.")
    return app

def API():
    """Runs the API."""
    app = create_app()
    debug_value = CONFIG["server"]["debug"]
    debug = False if debug_value.lower() == 'false' else True
    event_logger("API started.")
    app.run(host=CONFIG["server"]["host"], port=CONFIG["server"]["port"], debug=debug)

################
### Run Code ###
################

if __name__ == "__main__":
    event_logger("Starting API...") 
    scheduler = CONFIG["server"]["scheduler"]
    scheduler = False if scheduler.lower() == 'false' else True
    if scheduler:
        subprocess.Popen(["python", "scheduler.py"])
        event_logger("Scheduler started.") 
    API()
    event_logger("API stopped.")  
    