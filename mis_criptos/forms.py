from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, SubmitField, HiddenField
from wtforms.validators import ValidationError, DataRequired

class CryptoForm(FlaskForm):
    m_from = SelectField("From", validators=[DataRequired("Moneda obligatoria")], choices=[("EUR","EUR"), ("BTC", "BTC"),("ETH", "ETH"), ("USDT","USDT"), ("BNB", "BNB"), ("XRP", "XRP"), ("ADA", "ADA"), ("SOL", "SOL"), ("DOT", "DOT"), ("MATIC", "MATIC")])

    m_to = SelectField("To", validators=[DataRequired("Moneda obligatoria")], choices=[("EUR","EUR"), ("BTC", "BTC"),("ETH", "ETH"), ("USDT","USDT"), ("BNB", "BNB"), ("XRP", "XRP"), ("ADA", "ADA"), ("SOL", "SOL"), ("DOT", "DOT"), ("MATIC", "MATIC")])#las choises son lista de tuplas, lo primero será lo que viaja (el value), y lo segundo es lo que se vé

    q_from = FloatField("Cantidad", validators=[DataRequired("Cantidad obligatoria")])

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
    def valaidate_m_to(self,field):# al estar dentro de la clase no hace falta llamarla, la ejecuta automáticamente por llamarse validate_  y luego el nombre de la variable
        if self.data.m_from == "EUR":
'''