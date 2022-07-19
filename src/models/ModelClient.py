# Importa clase cliente from entities
from .entities.Client import Client
from flask import request

# Clase cliente con funciones
class ModelClient():

    @classmethod 
    def clientes(self, db, clientes):
        try:
            cursor = db.connection.cursor()
            sql = "Select * FROM clientes".format()
            cursor.execute(sql)
            row = cursor.fetchall()
            for x in row:
                print (x)
            return None
        except Exception as ex:
            return "didnt work"