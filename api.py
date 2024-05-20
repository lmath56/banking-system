# Lucas Mathews - Fontys Student ID: 5023572
# Banking System API

###############
### Modules ###
###############

import connexion # Imports connexion module
from config import CONFIG # Imports the configuration file
from manager import * # Imports the Manager file that contains the functions for the API
from flask import Flask, session, jsonify, request # Imports the Flask module
from flask_session import Session # Imports the session module 

#################
### Connexion ###
#################

def create_app():
    app = connexion.FlaskApp(__name__)
    app.add_api(CONFIG["api_file"]["name"])

    flask_app = app.app
    flask_app.config['SECRET_KEY'] = CONFIG["sessions"]["secret_key"]
    flask_app.config['SESSION_TYPE'] = 'filesystem'

    Session(flask_app)
    return app

def API():
    app = create_app()
    app.run(host=CONFIG["server"]["listen_ip"], port=CONFIG["server"]["port"], debug=CONFIG["server"]["debug"]) # Runs the API using the configuration file

################
### Run Code ###
################

if __name__ == "__main__":
    API()