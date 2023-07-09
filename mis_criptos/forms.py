from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, SubmitField
from wtforms.validators import ValidationError, DataRequired

class CryptoForm(FlaskForm):
    m_from = SelectField("From", validators=[DataRequired("Moneda obligatoria")], choices=[("EUR","EUR"), ("BTC", "BTC"),("ETH", "ETH"), ("USDT","USDT"), ("BNB", "BNB"), ("XRP", "XRP"), ("ADA", "ADA"), ("SOL", "SOL"), ("DOT", "DOT"), ("MATIC", "MATIC")])

    m_to = SelectField("To", validators=[DataRequired("Moneda obligatoria")], choices=[("EUR","EUR"), ("BTC", "BTC"),("ETH", "ETH"), ("USDT","USDT"), ("BNB", "BNB"), ("XRP", "XRP"), ("ADA", "ADA"), ("SOL", "SOL"), ("DOT", "DOT"), ("MATIC", "MATIC")])

    q_from = FloatField("Cantidad", validators=[DataRequired("Cantidad obligatoria")])