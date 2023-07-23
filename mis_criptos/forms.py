from mis_criptos import app
from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, SubmitField
from wtforms.validators import ValidationError, DataRequired
from mis_criptos.models import CryptosDAOsqlite

daoform = CryptosDAOsqlite(app.config.get("PATH_SQLITE"))#lo instanciamos en forms para poder hacer consultas en la BD

CRYPTOS = [("EUR","EUR"), ("BTC", "BTC"),("ETH", "ETH"), ("USDT","USDT"), ("BNB", "BNB"), ("XRP", "XRP"), ("ADA", "ADA"), ("SOL", "SOL"), ("DOT", "DOT"), ("MATIC", "MATIC")]

class CryptoForm(FlaskForm):
    m_from = SelectField("From", validators=[DataRequired("Moneda obligatoria")], choices=CRYPTOS)

    m_to = SelectField("To", validators=[DataRequired("Moneda obligatoria")], choices=CRYPTOS)#las choises son lista de tuplas, lo primero será lo que viaja (el value), y lo segundo es lo que se vé

    q_from = FloatField("Cantidad", validators=[DataRequired("Cantidad positiva obligatoria")]) 

    calculate = SubmitField("Calcular")
    buy = SubmitField("Compra")
    #hemos creado un formulario con WTForm con los campor requeridos con los validadores y los errores que se muestran al ponerlo mal, sinó podemos nada de mensaje se mostrará uno estándar en inglés. NO OLVIDAR DE IMPORTAR TOT

    
    def validate_m_from(self, field):#controlamos tener movimientos de esa cripto y si hay también que la cantidad sea mayor que 0
        if field.data !="EUR":
            q_from = 0
            q_to = 0
            self.total=0
            lista_to = daoform.quantity_to(field.data)
            if lista_to == [(None,None)]:
                raise ValidationError(f"No dispones de {field.data} para vender")
            else:                
                q_to += lista_to[0][1]
                
            lista_from = daoform.quantity_from(field.data)  
            if lista_from == [(None,None)]:
                pass
            else:
                q_from += lista_from[0][1]   

            self.total = q_to - q_from#guardo el total de lo comprado - lo vendido para saber la cantidad que me queda
            if self.total == 0:
                raise ValidationError(f"No dispones de {field.data} para vender")
 
    def validate_m_to(self, field):# al estar dentro de la clase no hace falta llamarla, la ejecuta automáticamente por llamarse validate_  y luego el nombre de la variable
        if self.m_from.data == "EUR" and field.data != "BTC":
            raise ValidationError("Solo puedes comprar BTC con Euros")
        if self.m_from.data == field.data:
            raise ValidationError("No puedes comprar la misma moneda")

    def validate_q_from(self, field):
        if field.data <= 0:
            raise ValidationError("Introduce una cantidad positiva")
        
        if self.m_from.data != "EUR" and self.total != 0:
            if field.data > self.total:#si la cantidad introducida es mayor a la cantidad de la que dispongo no me dejará vender
                raise ValidationError(f"No tienes suficientes {self.m_from.data} para vender")

    