from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required

from conect.config import config

# Modelos
from models.ModelUser import ModelUser

# Entities
from models.entities.User import User

app = Flask(__name__)

csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)

# funcion para retornar mediante id datos del usuario
@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

# Redirigir raiz a login
@app.route('/')
def index():
    return redirect(url_for('login'))

# Login - verificación usuario
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash('Contraseña invalida')
                return render_template('auth/login.html')
        else:
            flash("Usuario no encontrado")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

# Cerrar sesión
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# Vista home, need login
@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/clientes')
@login_required
def clientes():
    
    return render_template('auth/clientes_list.html')

@app.route('/clientes_add')
@login_required
def clientes_add():
    return render_template('auth/clientes_add.html')

@app.route('/mascotas')
@login_required
def mascotas():
    return render_template('auth/mascotas_list.html')


def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return "<h1> Lo sentimos, esta página no existe :( </h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()