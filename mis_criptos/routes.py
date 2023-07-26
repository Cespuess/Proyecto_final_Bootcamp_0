from mis_criptos import app
from flask import render_template, redirect, request, flash, session
from mis_criptos.models import Movement, CryptosDAOsqlite, Api
from mis_criptos.forms import CryptoForm
import sqlite3
from datetime import datetime, timezone

dao=CryptosDAOsqlite(app.config.get("PATH_SQLITE"))
api = Api() # instanciamos la clase de la petición a la API


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        try:
            movements= dao.get_all()
            return render_template("index.html", movements=movements, title="Mis movimientos", route=request.path)#el route lo pasamos para usarlo para desactivar el link del nav, el request.path devuelvela parte de la URL después del nombre de dominio.
        except (ValueError, sqlite3.OperationalError) as e:
            flash("Su fichero de datos está corrupto")
            flash(str(e))
            return render_template("index.html", movements=[], title="Mis Movimientos")

    else:
        try:
            movements= dao.get_all()#para mandar el mensaje de mov_ok
            mov_ok=True#para modificar en jinja el id del div de los mensajes flash
            flash("Compra realizada correctamente")
            return render_template("index.html", movements=movements, title="Mis movimientos", route=request.path, mov_ok=mov_ok) 
        except (ValueError, sqlite3.OperationalError) as e:
            flash("Su fichero de datos está corrupto")
            flash(str(e))
            return render_template("index.html", movements=[], title="Mis Movimientos")





@app.route("/purchase", methods=["GET", "POST"])# poniendo el methods se habilita el post, porque el get va siempre activado
def trading():
    form = CryptoForm()# instanciamos la clase del formulario vacío
    if request.method == "GET": 
        session["verification"]=[]#se crea una lista vacía para borrar los datos del cálculo anterior
        session["quantity_to"]="" #para que no nos dé problemas jinja
        return render_template("purchase.html", form=form, route=request.path, title="Trading")
    elif form.calculate.data:  # si el botón calcular ha sido el pulsado
        if form.validate():# si está bien validado, no solamente por las validaciones del navegador, sinó también por las funciones validadoras que se ejecutan después de pulsar los Submit
            try:
                api.get_rate(form.m_from.data, form.m_to.data, form.q_from.data)#hacemos la llamada a la API
            except (AttributeError, NameError) as e:
                api.error = str(e)
            
            if api.error:#solo entra si hay contenido en api.error
                flash(api.error)# capturamos el error que se haya podido procucir en la llamada a la API
                return render_template('purchase.html', form=form, route=request.path,title="Trading", api=api)
            
            #metemos todos los datos en las sessions para luego compararlos
            session["verification"] = [form.m_from.data, form.m_to.data, form.q_from.data, api.quantity_to]                    
            session["quantity_to"] = api.quantity_to
            session["time_calculate"] = datetime.now(timezone.utc)
            return render_template('purchase.html', form=form, route=request.path,title="Trading")
        
        else:
            session["quantity_to"] = ""#al no hacer el cálculo de la q_to por cualquier error borramos el dato que había de un posible cálculo correcto anterior para que no aparezca más
            return render_template("purchase.html", form=form, route=request.path, title="Trading")

    else:
        if dao.dos_minutos(session["time_calculate"]):#si pasan más de dos minutos entre el cálculo y la compra salta este error.
            flash("Han pasado más de dos minutos, vuelve a calcular la conversión.")
            session["quantity_to"] = "" 
            return render_template("purchase.html", form=form, route=request.path, title="Trading")
        elif session["verification"] != [form.m_from.data, form.m_to.data, form.q_from.data, session["quantity_to"]]: #si alguno ha sido modificado lanzamos un mensaje de error
            if session["quantity_to"] == "":#por si clica en comprar antes de calcular la conversión
                flash("Calcula la conversión antes de realizar una compra.")
                return render_template("purchase.html", form=form)
            else:
                flash("No modifiques los datos del cálculo antes de validar la compra. Vuelve a calcular la operación deseada.")
                session["quantity_to"] = ""#lo reiniciamos para que no se refleje en la pantalla el valor hecho antes 
                return render_template("purchase.html", form=form)
        else: 
            if form.validate():
                try:
                    date_form = session["time_calculate"]#guardamos en una variable el valor del datatime para luego sacar la fecha y el tiempo
                    date = date_form.strftime("%Y-%m-%d")
                    time = date_form.strftime("%X")
                    m = Movement(date, time, form.m_from.data, form.q_from.data, form.m_to.data, session["quantity_to"])#instanciamos el movimiento para incluirlo en la BD
                    dao.insert(m)# insertamos los datos del objeto recibido por el formulario

                    return redirect("/", code=307) # nos devuelve a la página inicial que nos muestra los movimientos, el code 307 envia temporalmente una solicitud POST.
                
                except (ValueError, sqlite3.OperationalError) as e: # por si el movimiento no se crea correctamente o se ha manipulado la llamada a la BD
                    flash(str(e))
                    return render_template('purchase.html', form=form, route=request.path,title="Trading")

            else:
                for msg in form.errors.values():#recorremos el diccionario que contiene los diferentes errores
                    flash(msg[0])#los grabamos uno x uno en flash
                session["quantity_to"] = ""#al no hacer el cálculo de la q_to por cualquier error borramos el dato que había de un posible cálculo correcto anterior para que no aparezca más
                return render_template("purchase.html", form=form, route=request.path, title="Trading")
                



@app.route("/status")
def wallet():
    
    try:
        lista_cantidad=api.get_value_eur(dao.get_status())
        
        if api.error:#solo entra si hay contenido en api.error
                    flash(api.error)# capturamos el error que se haya podido procucir en la llamada a la API
                    return render_template('status.html', route=request.path,title="Wallet", error=True)
        
        return render_template("status.html", route=request.path, title="Wallet", lista=lista_cantidad, error = False)
    
    except (AttributeError, sqlite3.OperationalError, NameError) as e:#controlamos errores generados por el usuario malvado
        flash(str(e))
        return render_template("status.html", route=request.path, title="Wallet", error=True)