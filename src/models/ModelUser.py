# Importa la clase User from entities
from .entities.User import User

class ModelUser():

    # classmethon para usarlo sin instanciar la clase ModelUser
    @classmethod
    def login(self,db,user):
        # En caso de que ocurra algo
        try:
            # Cursor para interactuar con la bd
            cursor = db.connection.cursor()
            # Comprobación de clave existente
            sql = "SELECT id, username, password, fullname FROM user WHERE username = '{}'".format(user.username)
            # Ejecutamos sql sentence
            cursor.execute(sql)
            # fila resultante
            row = cursor.fetchone()
            # Si existe usuario o no
            if row != None:
                # Verifico datos en bd y compruebo mediante la funcion check_password
                user = User(row[0], row[1], User.check_password(row[2], user.password), row[3]) 
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    #classmethod para capturar id usuario
    @classmethod
    def get_by_id(self,db,id):
        # En caso de que ocurra algo
        try:
            # Cursor para interactuar con la bd
            cursor = db.connection.cursor()
            # Comprobación de id existente
            sql = "SELECT id, username, fullname FROM user WHERE id = '{}'".format(id)
            # Ejecutamos sql sentence
            cursor.execute(sql)
            # fila resultante
            row = cursor.fetchone()
            # Si existe usuario o no
            if row != None:
                # Verifico datos en bd y compruebo 
                return User(row[0], row[1], None, row[2]) 
            else:
                return None
        except Exception as ex:
            raise Exception(ex)