from flask import Flask
from flask import render_template, redirect, url_for, request, flash

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('production.py')


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create", methods=['POST'])
def create():
    app.logger.debug(request.form['email'])
    return redirect(url_for("index"))
