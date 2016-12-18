from flask import Flask
from flask import render_template, redirect, url_for, request
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create", methods=['POST'])
def create():
    app.logger.debug(request.form['email'])
    return redirect(url_for("index"))
