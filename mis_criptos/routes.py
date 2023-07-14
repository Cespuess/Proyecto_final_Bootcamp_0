from mis_criptos import app
from flask import render_template, redirect, request, url_for, flash
from mis_criptos.models import Movement, CryptosDAOsqlite, Api
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
    api = Api() # instanciamos la clase con toda la info de la petición a la API
    if request.method == "GET": 
        return render_template("purchase.html", form=form, route=request.path, title="Trading")
    elif form.calculate.data:  # si el botón calcular ha sido el pulsado
        if form.validate():# si está bien validado, no solamente por las validaciones del navegador, sinó también por las funciones validadoras que se ejecutan después de pulsar los Submit
            api.get_rate(form.m_from.data, form.m_to.data, form.q_from.data)#hacemos la llamada a la API
            
            if api.error != False:#solo entra si hay contenido en api.error
                flash(api.error)# capturamos el error que se haya podido procucir en la llamada a la API
                return render_template('purchase.html', form=form, route=request.path,title="Trading", api=api)
            
            
            form.h_from.data = form.m_from.data #damos el valor correspondiente a los campos ocultos
            form.h_to.data = form.m_to.data
            form.h_q.data = form.q_from.data
            form.h_q_to.data = api.quantity_to
            form.h_date.data = api.date
            form.h_time.data = api.time            
            
            return render_template('purchase.html', form=form, route=request.path,title="Trading", api=api)
        
        else:
            return render_template("purchase.html", form=form, route=request.path, title="Trading")

    else:
        if form.h_from.data != form.m_from.data or form.h_to.data != form.m_to.data or form.h_q.data != str(form.q_from.data): #si alguno ha sido modificado lanzamos un mensaje de error
            flash("No modifiques los datos del cálculo antes de validar la compra.")
            return render_template("purchase.html", form=form)
        else: 
            if form.validate():
                try:
                    m = Movement(form.h_date.data, form.h_time.data, form.m_from.data, form.q_from.data, form.m_to.data, form.h_q_to.data)#instanciamos el movimiento para incluirlo en la BD
                    dao.insert(m)# insertamos los datos del objeto recibido por el formulario

                    return redirect("/") # nos devuelve a la página inicial que nos muestra los movimientos
                
                except ValueError as e:
                    flash(str(e))
                    return render_template('purchase.html', form=form, route=request.path,title="Trading")

            else:
                return render_template('purchase.html', form=form, route=request.path,title="Trading")



@app.route("/status")
def wallet():
    return render_template("status.html", route=request.path, title="Status")