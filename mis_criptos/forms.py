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

    calculate = SubmitField("Calcular")
    buy = SubmitField("Comprar")
    #hemos creado un formulario con WTForm con los campor requeridos con los validadores y los errores que se muestran al ponerlo mal, sinó podemos nada de mensaje se mostrará uno estándar en inglés. NO OLVIDAR DE IMPORTAR TOT