from mis_criptos import app
import sqlite3
import requests
from decimal import Decimal #importamos para que no nos dé el error al comprar pequeñas cantidades ej:0.0000042 evitará que sea 4.2e6

CRYPTOS = ["EUR","ADA", "BNB", "BTC", "DOT", "ETH", "MATIC", "SOL", "USDT", "XRP"]

class Movement:
    def __init__(self, input_date, time, moneda_from, cantidad_from, moneda_to, cantidad_to, id=None):
        self.date= input_date
        self.time= time
        self.moneda_from=moneda_from
        self.cantidad_from=cantidad_from
        self.moneda_to=moneda_to
        self.cantidad_to=cantidad_to
        self.id=id
        

    def __eq__(self, other):
        return self.id == other.id and self.date == other.date and self.time == other.time and self.moneda_from == other.moneda_from and self.cantidad_from == other.cantidad_from and self.moneda_to == other.moneda_to and self.cantidad_to == other.cantidad_to
    
    def __repr__(self):
        return f"objeto Movement {self.id} {self.date} {self.time} {self.moneda_from} {self.cantidad_from} {self.moneda_to} {self.cantidad_to}"
    
    def __str__(self):
        return self.__repr__()

class Api:
    def __init__(self):
        pass

    def get_rate(self, moneda_from, moneda_to, quantity):
        self.moneda_from = moneda_from
        self.moneda_to = moneda_to
        self.quantity_from = quantity
        self.error = False
        url = f'https://rest.coinapi.io/v1/exchangerate/{self.moneda_from}/{self.moneda_to}?apikey={app.config.get("API_KEY")}'


        try:
            response = requests.get(url)#se ejecuta la petición
            data = response.json()# hemos creado un diccionario con el texto de la respuesta del json

            if response.status_code == 200: # pedimos el código de respuesta para estar seguros de que si la petición ha ido bien poder hacer los cálculos necesarios
                rate = Decimal(data["rate"])# utilizamos el módulo Decimal para que nos de el número en decimales y no en notación científica
                self.quantity_to = Decimal(self.quantity_from) * rate
                #self.date, self.time = self.get_time(data["time"])
            elif response.status_code == 400: 
                self.error = "Solicitud incorrecta: hay algún problema con su solicitud"
            elif response.status_code == 401: 
                self.error = "API KEY incorrecta"
            elif response.status_code == 403: 
                self.error = "API KEY sin suficientes recursoso para acceder al recurso solicitado"
            elif response.status_code == 429: 
                self.error = "Límite de solicitudes excedido"
            elif response.status_code == 550: 
                self.error = "Sin datos: no disponemos el artículo que nos solicitó en este momento"  
            else:
                self.error = data["error"] 

        except requests.exceptions.RequestException as e:
            self.error = str(e)

    def get_value_eur(self, lista):
        self.error = False
        url = f'https://rest.coinapi.io/v1/exchangerate/EUR?apikey={app.config.get("API_KEY")}'

        try:
            response = requests.get(url)
            data = response.json()
            if response.status_code == 200:
                if data["rates"] != []:#si alguien modifica la parte EUR de la url esto ayudará a que no pete la app
                    for lista_currency in lista:#recorremos moneda por moneda de las que tenemos
                        for cripto in data["rates"]: # recorremos las monedas de la solicitud API
                            if lista_currency[0] == cripto["asset_id_quote"]: #a la que encuentra la información de nuestra moneda dividimos nuestra cantidad por el rate para obtener nuestro valor en euros y lo añadimos en la lista ["ADA",25,55]
                                a = lista_currency[1] / cripto["rate"]
                                lista_currency.append(a)
                
                else:
                    self.error = "Verifique la url de llamada a la API"
                            
            elif response.status_code == 400: 
                self.error = "Solicitud incorrecta: hay algún problema con su solicitud"
            elif response.status_code == 401: 
                self.error = "API KEY incorrecta"
            elif response.status_code == 403: 
                self.error = "API KEY sin suficientes recursoso para acceder al recurso solicitado"
            elif response.status_code == 429: 
                self.error = "Límite de solicitudes excedido"
            elif response.status_code == 550: 
                self.error = "Sin datos: no disponemos el artículo que nos solicitó en este momento"
            else: 
                self.error = data["error"]


            return lista

        except requests.exceptions.RequestException as e:
            self.error = str(e)
    

class CryptosDAOsqlite: #data acces object (para guardar los datos)
    def __init__(self, db_path):
        self.path=db_path

        query="""CREATE TABLE IF NOT EXISTS "movements" (
        "id"	INTEGER,
        "date"	TEXT NOT NULL,
        "time"	TEXT NOT NULL,
        "moneda_from"	TEXT NOT NULL,
        "cantidad_from"	REAL NOT NULL,
        "moneda_to"	TEXT NOT NULL,
        "cantidad_to"	REAL NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT)
        )
        """#el if not exist hace que la crea si aún no existe

        conn=sqlite3.connect(self.path)# establece la conexión con la BD, si el fichero no existe lo crea.
        cur=conn.cursor()#es el objeto que permite manipular la BD 
        cur.execute(query)# el execute crea la tabla en la BD con los valores del create, que los habíamos guardado en la variable query
        conn.close()#cerrar siempre la conexión para liberar recursos y evitar problemas


    def get_all(self):
        query="""
        SELECT  date, time, moneda_from, cantidad_from, moneda_to, cantidad_to, id FROM movements ORDER by date, time;
        """

        conn=sqlite3.connect(self.path)
        cur=conn.cursor()
        cur.execute(query)
        res=cur.fetchall() # devuelve una lista de tuplas con la resta de la consulta 
        lista = [Movement(*reg) for reg in res]# crea una lista con primero lo que se quiere añadir y luego lo que se recorre  esto se llama LIST COMPREHENSION

        conn.close()
        return lista

    def insert(self, movement):
        query= """
        INSERT INTO movements (date, time, moneda_from, cantidad_from, moneda_to, cantidad_to) VALUES (?,?,?,?,?,?)
        """
        conn= sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(query, (movement.date, movement.time, movement.moneda_from, movement.cantidad_from, movement.moneda_to, movement.cantidad_to))
        conn.commit()
        conn.close()

    def quantity_to(self,currency):
        query= """
        SELECT moneda_to, SUM(cantidad_to) FROM movements
        WHERE moneda_to = ?
        """

        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(query, (currency,))
        res = cur.fetchall()
        conn.close()
        return res
    
    def quantity_from(self,currency):
        query= """
        SELECT moneda_from, SUM(cantidad_from) FROM movements
        WHERE moneda_from = ?
        """

        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(query, (currency,))
        res = cur.fetchall()
        conn.close()
        return res

    def get_status(self):#recorremos cada cripto para que nos devuelva una lista de listas con la moneda, valor, de las que dispongamos
        lista_status=[]
        for cripto in CRYPTOS:
            q_to=0
            q_from=0
            lista_to= self.quantity_to(cripto)
            if lista_to == [(None,None)]:
                pass
            else:
                q_to += lista_to[0][1]

            lista_from = self.quantity_from(cripto)
            if lista_from == [(None,None)]:
                pass
            else:
                q_from += lista_from[0][1]

            total = q_to - q_from

            if total != 0 or cripto == "EUR": #aunque EUR sea 0 lo necesitamos para el valor en la página
                lista_status.append([cripto,total])

        return lista_status








    
