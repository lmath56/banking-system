from flask import Flask, render_template, request
import requests

SERVER_URL = "http://127.0.0.1:8000"

app = Flask(__name__)

@app.route("/", methods=["GET"])
def loginGET():
    return render_template("login.html")

@app.route("/", methods=["POST"])
def loginPOST():
    username = request.form["username"]
    password = request.form["password"]
    response = requests.get( f"{SERVER_URL}/login?username={username}&password={password}")
    return render_template("succes.html", data = response.content)

app.run()