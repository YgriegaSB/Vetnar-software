from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required

# conexion bd
from conect.config import config

# Modelos
from models.ModelUser import ModelUser
from models.ModelClient import ModelClient

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

######################### Verificacion user y login #############################
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
######################### Cerrar sesión #############################
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

################################################# Vistas home ###########################################################
# Vista home, need login
@app.route('/home')
@login_required
def home():
    return render_template('home.html')

################################################# Vistas cliente ###########################################################
########################## Listar clientes #############################
@app.route('/clientes')
@login_required
def clientes():
    cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM clientes')
    data = cursor.fetchall()
    print (data)
    return render_template('auth/clientes_list.html', clientes = data)
######################################################
# Redirigir a create_add
@app.route('/clientes_add')
@login_required
def clientes_add():
    return render_template('auth/clientes_add.html')

@app.route('/create_cl', methods=['POST'])
@login_required
def create():
    if request.method == 'POST':
        # recibir datos
        nombrecl = request.form['nombre_cl']
        rutcl = request.form['rut_cl']
        cumpleañoscl = request.form['cumpleaños_cl']
        registrocl = request.form['registro_cl']
        telefonofcl = request.form['telefonoC']
        telefonomcl = request.form['telefonoM']
        telefonotcl = request.form['telefonoT']
        correocl = request.form['correo_cl']
        facebookcl = request.form['facebook_cl']
        derivado = request.form['derivado']
        direccioncl = request.form['direccion_cl']
        referencias = request.form['referencias']
        notas = request.form['notas']
        # conexion bd
        cursor = db.connection.cursor()
        # sql sentence
        cursor.execute('INSERT INTO clientes (nombre_cl, rut_cl, cumpleaños_cl, fecha_registro, telefono_casa, telefono_movil, telefono_trabajo, correo_cl, facebook_cl, derivado, direccion_cl, referencias_direc, notas_cl) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s)', (nombrecl, rutcl,
        cumpleañoscl, registrocl, telefonofcl, telefonomcl, telefonotcl, correocl, facebookcl, derivado, direccioncl, referencias, notas))
        # commit sql sentence
        db.connection.commit()
        # message
        return redirect(url_for('clientes'))        

######################################################
# Redirigir a clientes_info
@app.route('/clientes_info')
@login_required
def clientes_info():
    return render_template('auth/clientes_info.html')
######################################################
# Redirigir a clientes_edit
@app.route('/clientes_edit')
@login_required
def clientes_edit():
    return render_template('auth/clientes_edit.html')
######################################################
# Redirigir a clientes_mascotas
@app.route('/clientes_mascotas')
@login_required
def clientes_mascotas():
    return render_template('auth/clientes_mascotas.html')
########################## Create  from clientes_add #############################
@app.route('/create_cl', methods=['POST'])
def create_cl():
    if request.method == 'POST':

        return ModelClient.create_cl(db, clientes)
    else:
        return render_template('auth/clientes_add.html')

################################################# Vistas mascotas ###########################################################
@app.route('/mascotas')
@login_required
def mascotas():
    return render_template('auth/mascotas_list.html')
######################################################
@app.route('/mascotas_add')
@login_required
def mascotas_add():
    return render_template('auth/mascotas_add.html')
######################################################
@app.route('/mascotas_razas')
@login_required
def mascotas_razas():
    return render_template('auth/mascotas_razas.html')
######################################################
@app.route('/mascotas_info')
@login_required
def mascotas_info():
    return render_template('auth/mascotas_info.html')
######################################################
@app.route('/mascotas_edit')
@login_required
def mascotas_edit():
    return render_template('auth/mascotas_edit.html')
######################################################
@app.route('/mascotas_history')
@login_required
def mascotas_history():
    return render_template('auth/mascotas_history.html')
################################################# Vistas historial  ###########################################################
################################################# Vistas historial  ###########################################################
################################################# Vistas config     ###########################################################

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