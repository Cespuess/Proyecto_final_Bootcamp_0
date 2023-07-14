from mis_criptos import app
from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, SubmitField, HiddenField
from wtforms.validators import ValidationError, DataRequired
from mis_criptos.models import CryptosDAOsqlite

daoform = CryptosDAOsqlite(app.config.get("PATH_SQLITE"))

CRYPTOS = [("EUR","EUR"), ("BTC", "BTC"),("ETH", "ETH"), ("USDT","USDT"), ("BNB", "BNB"), ("XRP", "XRP"), ("ADA", "ADA"), ("SOL", "SOL"), ("DOT", "DOT"), ("MATIC", "MATIC")]

class CryptoForm(FlaskForm):
    m_from = SelectField("From", validators=[DataRequired("Moneda obligatoria")], choices=CRYPTOS)

    m_to = SelectField("To", validators=[DataRequired("Moneda obligatoria")], choices=CRYPTOS)#las choises son lista de tuplas, lo primero será lo que viaja (el value), y lo segundo es lo que se vé

    q_from = FloatField("Cantidad", validators=[DataRequired("Cantidad positiva obligatoria")])

    h_from = HiddenField() # creamos los campos ocultos para poner comparar luego anter de validar
    h_to = HiddenField()
    h_q = HiddenField()

    h_q_to = HiddenField()
    h_date = HiddenField()
    h_time = HiddenField()

    calculate = SubmitField("Calcular")
    buy = SubmitField("Comprar")
    #hemos creado un formulario con WTForm con los campor requeridos con los validadores y los errores que se muestran al ponerlo mal, sinó podemos nada de mensaje se mostrará uno estándar en inglés. NO OLVIDAR DE IMPORTAR TOT

    '''
    def validate_m_from(self, field):
        if field.data !="EUR":
            res, lista = daoform.get_all
            q_from = 0
            q_to = 0
            for m in lista:
                if field.data in m.moneda_from:
                    q_from += m.cantidad_from
                if field.data in m.moneda_to:
                    q_to += m.cantidad_to
            total = q_to - q_from
            if total == 0:
                raise ValidationError(f"No dispones de {field.data} para vender")
    '''     


    def validate_m_to(self, field):# al estar dentro de la clase no hace falta llamarla, la ejecuta automáticamente por llamarse validate_  y luego el nombre de la variable
        if self.m_from.data == "EUR" and field.data != "BTC":
            raise ValidationError("Solo puedes comprar BTC con Euros")
        


        
    def validate_q_from(self, field):
        if field.data <= 0:
            raise ValidationError("Introduce una cantidad positiva")

    