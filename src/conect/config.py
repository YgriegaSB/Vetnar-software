# Contraseña
class Config:
    SECRET_KEY = 'B!1weNAt1T^%kvhUI*S^'

# Clase para depuración
class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_USER = 'root'
    MYSQL_HOST = 'localhost'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'vet'

config = {
    'development' : DevelopmentConfig
}