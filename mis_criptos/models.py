from mis_criptos import app
import sqlite3
import requests
from decimal import Decimal #importamos para que no nos dé el error al comprar pequeñas cantidades ej:0.0000042 evitará que sea 4.2


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
        self.url = f'https://rest.coinapi.io/v1/exchangerate/{self.moneda_from}/{self.moneda_to}?apikey={app.config.get("API_KEY")}'


        try:
            response = requests.get(self.url)#se ejecuta la petición
            data = response.json()# hemos creado un diccionario con el texto de la respuesta del json

            if response.status_code == 200: # pedimos el código de respuesta para estar seguros de que si la petición ha ido bien poder hacer los cálculos necesarios
                rate = Decimal(data["rate"])
                print(rate)
                self.quantity_to = Decimal(self.quantity_from) * rate
                self.date, self.time = self.get_time(data["time"])
                
            else:
                self.error = data["error"] 

        except requests.exceptions.RequestException as e:
            self.error = str(e)

    def get_time(self, cadena): # recorremos la cadena para separar fecha y tiempo de la llamada a la API
        d= cadena[:10]
        t= cadena[11:19]
        return d, t

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
        "cantidad_to"	NUMERIC NOT NULL,
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
        SELECT moneda_to, cantidad_to FROM movements
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
        SELECT moneda_from, cantidad_from FROM movements
        WHERE moneda_from = ?
        """

        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(query, (currency,))
        res = cur.fetchall()
        conn.close()
        return res


