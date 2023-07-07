from mis_criptos import app
from flask import render_template, redirect, request, url_for


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/purchase")
def trading():
    return render_template("purchase.html")

@app.route("/status")
def wallet():
    return render_template("status.html")