from mis_criptos import app
from flask import render_template, redirect, request, url_for, flash
from mis_criptos.models import Movement, CryptosDAOsqlite

dao=CryptosDAOsqlite(app.config.get("PATH_SQLITE"))

@app.route("/")
def index():

    try:
        movements= dao.get_all()
        return render_template("index.html", movements=movements, title="Mis movimientos", route=request.path)
    except ValueError as e:
        flash("Su fichero de datos está corrupto")
        flash(str(e))
        return render_template("index.html", movements=[], title="Mis Movimientos")






@app.route("/purchase")
def trading():
    return render_template("purchase.html", route=request.path, title="Trading")





@app.route("/status")
def wallet():
    return render_template("status.html", route=request.path, title="Status")