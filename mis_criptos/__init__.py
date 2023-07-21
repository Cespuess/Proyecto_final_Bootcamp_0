from flask import Flask

app = Flask(__name__)
app.config.from_prefixed_env()#se utiliza para cargar la configuración de una aplicación Flask desde variables de entorno con un prefijo común.
