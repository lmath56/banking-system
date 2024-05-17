# Lucas Mathews - Fontys Student ID: 5023572
# Banking System API

###############
### Modules ###
###############

import connexion # Imports connexion module
from config import CONFIG # Imports the configuration file
from manager import * # Imports the Manager file that contains the functions for the API

#################
### Connexion ###
#################

def API():
    app = connexion.FlaskApp(__name__)
    app.add_api(CONFIG["api_file"]["name"])
    app.run(host=CONFIG["server"]["listen_ip"], port=CONFIG["server"]["port"], debug=CONFIG["server"]["debug"]) # Runs the API using the configuration file

################
### Run Code ###
################

if __name__ == "__main__":
    API()