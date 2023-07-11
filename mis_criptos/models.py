import sqlite3
import os
from datetime import date, time 

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

