# Lucas Mathews - Fontys Student ID: 5023572
# Banking System Flask App

from flask import Flask, render_template, request, make_response, redirect

from config import CONFIG

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('bank/index.html')

