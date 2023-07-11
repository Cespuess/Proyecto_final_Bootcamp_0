from mis_criptos import app
from flask import render_template, redirect, request, url_for, flash
from mis_criptos.models import Movement, CryptosDAOsqlite
from mis_criptos.forms import CryptoForm

dao=CryptosDAOsqlite(app.config.get("PATH_SQLITE"))

@app.route("/")
def index():

    try:
        movements= dao.get_all()
        return render_template("index.html", movements=movements, title="Mis movimientos", route=request.path)#el route lo pasamos para usarlo para desactivar el link del nav, el request.path devuelvela parte de la URL después del nombre de dominio.
    except ValueError as e:
        flash("Su fichero de datos está corrupto")
        flash(str(e))
        return render_template("index.html", movements=[], title="Mis Movimientos")






@app.route("/purchase", methods=["GET", "POST"])# poniendo el methods se habilita el post, porque el get va siempre activado
def trading():
    form = CryptoForm()# instanciamos la clase del formulario vacío
    if request.method == "GET": 
        return render_template("purchase.html", form=form, route=request.path, title="Trading")
    elif form.calculate.data: #damos el valor correspondiente a los campos ocultos 
        form.h_from.data = form.m_from.data
        form.h_to.data = form.m_to.data
        form.h_q.data = form.q_from.data
        return render_template('purchase.html', form=form)
    else:
        if form.h_from.data != form.m_from.data or form.h_to.data != form.m_to.data or form.h_q.data != str(form.q_from.data): #si alguno ha sido modificado lanzamos un mensaje de error
            flash("No modifiques los datos del cálculo antes de validar la compra.")
            return render_template("purchase.html", form=form)
        else: 
            pass




@app.route("/status")
def wallet():
    return render_template("status.html", route=request.path, title="Status")