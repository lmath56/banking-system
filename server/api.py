# Lucas Mathews - Fontys Student ID: 5023572
# Banking System API

###############
### Modules ###
###############

import threading
import connexion # Imports connexion module
from config import CONFIG # Imports the configuration file
from manager import * # Imports the Manager file that contains the functions for the API
from flask_session import Session # Imports the session module 
from scheduler import run_schedule # Imports the scheduler module

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
    return app

def API():
    """Runs the API."""
    app = create_app()
    debug_value = CONFIG["server"]["debug"]
    debug = False if debug_value.lower() == 'false' else True
    app.run(host=CONFIG["server"]["host"], port=CONFIG["server"]["port"], debug=debug)

################
### Run Code ###
################

if __name__ == "__main__":
    event_logger("Starting API...") # Create a thread that will run the run_schedule function in the background
    scheduler = CONFIG["server"]["scheduler"]
    scheduler = False if scheduler.lower() == 'false' else True
    if scheduler:
        thread = threading.Thread(target=run_schedule)
        thread.daemon = True  # Set the thread as a daemon thread
        thread.start()
        event_logger("Scheduler started.") 
    API()
    event_logger("API stopped.")  # This line will only be reached if the API is stopped
    