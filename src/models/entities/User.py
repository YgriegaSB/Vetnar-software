# Importo metodo para mantener las contraseñas más seguras
from werkzeug.security import check_password_hash
# importo usermixin para detectar usuario activo
from flask_login import UserMixin

# Clase con metodo __init__ que funciona como reflejo de la bd, recibiendo los datos
class User(UserMixin):
    def __init__(self, id, username,  password, fullname="") -> None:
        self.id = id
        self.username = username
        self.password = password
        self.fullname = fullname

    # Metodo para recibir passwd hasheado y passwd
    # Metodo sin necesidad de instanciar clase (@classmethod)
    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)