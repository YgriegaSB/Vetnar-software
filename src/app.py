from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import  generate_password_hash

# conexion bd
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
    return render_template('auth/adirectos.html')

################################################# Vistas cliente ###########################################################
########################## Listar clientes #############################
@app.route('/clientes')
@login_required
def clientes():
    cursor = db.connection.cursor()
    cursor.execute('SELECT id_cliente, nombre_cl, rut_cl, telefono_movil, correo_cl, direccion_cl FROM clientes')
    data = cursor.fetchall()
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
        flash('Cliente agregado exitosamente') 
        return redirect(url_for('clientes_add'))        

######################### Clientes info #############################
@app.route('/perfil_cl/<id_cliente>')
@login_required
def perfil_cl(id_cliente):
    cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM clientes WHERE id_cliente = {}'. format(id_cliente))
    data = cursor.fetchall()
    return render_template('auth/clientes_info.html', cliente = data[0])

######################### Clientes edit #############################
@app.route('/edit_client/<id_cliente>')
@login_required
def clientes_edit(id_cliente):
    cursor = db.connection.cursor()
    cursor.execute('SELECT id_cliente, nombre_cl, rut_cl, cumpleaños_cl, fecha_registro, telefono_casa, telefono_movil, telefono_trabajo, correo_cl, facebook_cl, derivado, direccion_cl, referencias_direc, notas_cl FROM clientes WHERE id_cliente = {}'. format(id_cliente))
    data = cursor.fetchall()
    return render_template('auth/clientes_edit.html', cliente = data[0])

@app.route('/update_cl/<id_cliente>', methods=['POST'])
@login_required
def edit_cl(id_cliente):
    if request.method == 'POST':    
        nombrecl = request.form['nombre_cl']
        rutcl = request.form['rut_cl']
        cumpleañoscl = request.form['cumpleaños_cl']
        registrocl = request.form['registro_cl']
        telefonofcl = request.form['telefonoC']
        telefonomcl = request.form['telefonoM']
        telefonotcl = request.form['telefonoT']
        correo_cl = request.form['correo_cl']
        facebookcl = request.form['facebook_cl']
        derivado = request.form['derivado']
        direccioncl = request.form['direccion_cl']
        referencias = request.form['referencias']
        notas = request.form['notas']
        cursor = db.connection.cursor()
        cursor.execute = (""" 
        UPDATE clientes
        SET nombre_cl = %s,
            rut_cl = %s,
            cumpleaños_cl = %s,
            fecha_registro = %s,
            telefono_casa = %s,
            telefono_movil = %s,
            telefono_trabajo = %s,
            correo_cl = %s,
            facebook_cl = %s,
            derivado = %s,
            direccion_cl = %s,
            referencias_direc = %s,
            notas_cl = %s
        WHERE id_cliente = %s
        """, (nombrecl, rutcl, cumpleañoscl, registrocl, telefonofcl, telefonomcl, 
        telefonotcl, correo_cl, facebookcl, derivado, direccioncl, referencias, notas, id_cliente))
        db.connection.commit()
        flash('Cliente actualizado satisfactoriamente')
        return redirect(url_for('clientes'))

######################### Clientes delete #############################
@app.route('/delete_cl/<string:id_cliente>')
def delete_cl(id_cliente):
    cur = db.connection.cursor()
    cur.execute('DELETE FROM clientes WHERE id_cliente = {}'. format(id_cliente))
    db.connection.commit()
    flash('Cliente removido satisfactoriamente')    
    return redirect(url_for('clientes'))
######################################################
# Redirigir a clientes_mascotas
@app.route('/clientes_mascotas')
@login_required
def clientes_mascotas():
    return render_template('auth/clientes_mascotas.html')

################################################# Vistas mascotas ###########################################################
@app.route('/mascotas')
@login_required
def mascotas():
    cursor = db.connection.cursor()
    cursor.execute('SELECT id_mascota, dueño, nombre_m, nacimiento, chip, especie, notas FROM mascotas')
    data = cursor.fetchall()
    return render_template('auth/mascotas_list.html', mascotas = data)

# redirect a mascotas_add
@app.route('/mascotas_add')
@login_required
def mascotas_add():
    return render_template('auth/mascotas_add.html')

# Buscador propietario 
#@app.route("/search_cl", methods=['GET', 'POST'])
#@login_required
#def search():
#    cursor = db.connection.cursor()
#    sql = "SELECT nombre_cl FROM clientes"
#    cursor.execute(sql)
#    clientes = cursor.fetchall()
#    print(clientes)
#    return render_template('auth/mascotas_add.html', clientes = clientes)

@app.route('/create_pet', methods=['GET','POST'])
@login_required
def create_pet():
    if request.method == 'POST':
        nombre = request.form['clientes']
        paciente = request.form['paciente']
        nacimiento = request.form['nacimiento']
        microchip = request.form['chip']
        especie = request.form['especie']
        raza = request.form['raza']
        sexo = request.form['sexo']
        castrado = request.form['castrado']
        asegurado = request.form['asegurado']
        notas = request.form['notas']
        # conexion bd
        cursor = db.connection.cursor()
        # sentencia sql
        cursor.execute('INSERT INTO mascotas (dueño,nombre_m,nacimiento,chip,especie,raza,sexo,castrado,asegurado,notas) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (nombre, paciente, nacimiento,microchip, especie, raza, sexo,castrado,asegurado,notas))
        # commit sql sentence
        db.connection.commit()
        # message
        flash('Paciente agregado exitosamente') 
        return redirect(url_for('mascotas_add'))

# Perfil
@app.route('/perfil_pet/<id_mascota>')
@login_required
def perfil_pet(id_mascota):
    cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM mascotas WHERE id_mascota = {}'. format(id_mascota))
    data = cursor.fetchall()
    return render_template('auth/mascotas_info.html', mascota = data[0])

# Editar
@app.route('/edit_pet/<id_mascota>')
def get_pet(id_mascota):
    cursor = db.connection.cursor()
    cursor.execute('SELECT id_mascota, dueño, nombre_m, nacimiento, chip, especie, raza, sexo, castrado, asegurado, notas FROM mascotas WHERE id_mascota = {}'. format(id_mascota))
    data = cursor.fetchall()
    return render_template('auth/mascotas_edit.html', mascota = data[0])
# upgrade
@app.route('/update_pet/<id_mascota>', methods = ['POST'])
def update_pet(id_mascota):
    if request.method == 'POST':
        dueño = request.form['clientes']
        nombrem = request.form['paciente']
        nacimiento = request.form['nacimiento']
        chip = request.form['chip']
        especie = request.form['especie']
        raza = request.form['raza']
        sexo = request.form['sexo']
        castrado = request.form['castrado']
        asegurado = request.form['asegurado']
        notas = request.form['notas']
        cur = db.connection.cursor()
        cur.execute( """
        UPDATE mascotas
        SET dueño = %s,
            nombre_m = %s,
            nacimiento = %s,
            chip = %s,
            especie = %s,
            raza = %s,
            sexo = %s,
            castrado = %s,
            asegurado = %s,
            notas = %s
        WHERE id_mascota = %s
        """, (dueño, nombrem, nacimiento, chip, especie, raza, sexo, castrado, asegurado, notas, id_mascota))
        db.connection.commit()
        flash('Paciente actualizado satisfactoriamente')
        return redirect(url_for('mascotas_add'))
        
################# Mascotas delete ####################
@app.route('/delete_pet/<string:id_mascota>')
def delete_pet(id_mascota):
    cur = db.connection.cursor()
    cur.execute('DELETE FROM mascotas WHERE id_mascota = {}'. format(id_mascota))
    db.connection.commit()
    flash('Paciente removido satisfactoriamente')    
    return redirect(url_for('mascotas'))
######################################################
@app.route('/mascotas_info')
@login_required
def mascotas_info():
    return render_template('auth/mascotas_info.html')
################################################# Vistas historial  ###########################################################
@app.route('/mascotas_history')
@login_required
def mascotas_history():
    return render_template('auth/mascotas_history.html')
################################################# Vistas servicios  ###########################################################
@app.route('/servicios')
@login_required
def servicios_list():
    cursor = db.connection.cursor()
    cursor.execute('SELECT id_servicio, nombre, precio FROM servicios')
    data = cursor.fetchall()
    return render_template('auth/servicios.html', servicios = data)
################ Add servicio ################
@app.route('/servicios_add')
@login_required
def servicios_add():
    return render_template('auth/servicios_add.html')

@app.route('/create_service', methods=['GET','POST'])
@login_required
def create_ser():
    if request.method == 'POST':
        nombre = request.form['servicio']
        precio = request.form['precio']
        cursor = db.connection.cursor()
        cursor.execute('INSERT INTO servicios (nombre, precio) VALUES (%s, %s)', (nombre, precio))
        # commit sql sentence
        db.connection.commit()
        # message
        flash('Servicio agregado exitosamente') 
        return redirect(url_for('servicios_add'))

# Editar
@app.route('/edit_serv/<id_servicio>')
def get_serv(id_servicio):
    cursor = db.connection.cursor()
    cursor.execute('SELECT id_servicio, nombre, precio FROM servicios WHERE id_servicio = {}'. format(id_servicio))
    data = cursor.fetchall()
    return render_template('auth/servicios_edit.html', servicio = data[0])
# upgrade
@app.route('/update_service/<id_servicio>', methods = ['POST'])
def update_service(id_servicio):
    if request.method == 'POST':
        nombre = request.form['servicio']
        precio = request.form['precio']
        cur = db.connection.cursor()
        cur.execute("""
        UPDATE servicios
        SET nombre = %s,
            precio = %s
        WHERE id_servicio = %s
        """, (nombre, precio, id_servicio))
        db.connection.commit()
        flash('Servicio actualizado satisfactoriamente')
        return redirect(url_for('servicios_add'))
 
# Eliminar
@app.route('/delete_serv/<string:id_servicio>')
def delete_serv(id_servicio):
    db.connection.commit()
    cur = db.connection.cursor()
    cur.execute('DELETE FROM servicios WHERE id_servicio = {}'. format(id_servicio))
    flash('Profesional removido satisfactoriamente')    
    return redirect(url_for('servicios_add'))

################################################# Vistas profesionales  ###########################################################
@app.route('/profesionales')
@login_required
def profesionales_list():
    cursor = db.connection.cursor()
    cursor.execute('SELECT id_profesional, nombre, apellidoP, apellidoM, especialidad FROM profesionales')
    data = cursor.fetchall()
    return render_template('auth/profesionales.html', profesionales = data)

@app.route('/profesionales_add')
@login_required
def profesionales_add():
    return render_template('auth/profesionales_add.html')
################ Agregar profesional ################
@app.route('/create_expert', methods=['GET','POST'])
@login_required
def create_exp():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidop = request.form['apellidoP']
        apellidom = request.form['apellidoM']
        especialidad = request.form['especialidad']
        cursor = db.connection.cursor()
        cursor.execute('INSERT INTO profesionales (nombre, apellidoP, apellidoM, especialidad) VALUES (%s, %s, %s, %s)', (nombre, apellidop, apellidom, especialidad))
        # commit sql sentence
        db.connection.commit()
        # message
        flash('Profesional agregado exitosamente') 
        return redirect(url_for('profesionales_add'))
# Editar
@app.route('/edit_expert/<id_profesional>')
def get_expert(id_profesional):
    cursor = db.connection.cursor()
    cursor.execute('SELECT id_profesional, nombre, apellidoP, apellidoM, especialidad FROM profesionales WHERE id_profesional = {}'. format(id_profesional))
    data = cursor.fetchall()
    return render_template('auth/profesionales_edit.html', profesional = data[0])
# upgrade
@app.route('/update_expert/<id_profesional>', methods = ['POST'])
def update_expert(id_profesional):
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidoP = request.form['apellidoP']
        apellidoM = request.form['apellidoM']
        especialidad = request.form['especialidad']
        cur = db.connection.cursor()
        cur.execute( """
        UPDATE profesionales
        SET nombre = %s,
            apellidoP = %s,
            apellidoM = %s,
            especialidad = %s
        WHERE id_profesional = %s
        """, (nombre, apellidoP, apellidoM, especialidad, id_profesional))
        db.connection.commit()
        flash('Profesional actualizado satisfactoriamente')
        return redirect(url_for('profesionales_add'))

@app.route('/delete_expert/<string:id_profesional>')
def delete_expert(id_profesional):
    cur = db.connection.cursor()
    cur.execute('DELETE FROM profesionales WHERE id_profesional = {}'. format(id_profesional))
    db.connection.commit()
    flash('Profesional removido satisfactoriamente')    
    return redirect(url_for('profesionales_add'))
        
################################################# Vistas settings     ###########################################################
@app.route('/settings')
@login_required
def settings():
    return render_template('auth/settings.html')

@app.route('/usuarios_list')
@login_required
def user_list():
    cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM user')
    data = cursor.fetchall()
    return render_template('auth/user_list.html', user = data)

@app.route('/usuarios_add')
@login_required
def usuarios_add():
    return render_template('auth/user_add.html')

################ Agregar profesional ################
@app.route('/user_add', methods=['GET','POST'])
@login_required
def create_user():
    if request.method == 'POST':
        # Recepcion de datos form
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        nombre = request.form['nombre']
        rol = request.form['rol']
        movil = request.form['movil']
        domicilio = request.form['domicilio']
        # Hasheo de pássword
        password_hashed = generate_password_hash(contraseña)
        cursor = db.connection.cursor()
        cursor.execute('INSERT INTO user (username, password, fullname, rol, t_movil, domicilio) VALUES (%s, %s, %s, %s, %s, %s)', (correo, password_hashed, nombre, rol, movil, domicilio))
        # commit sql sentence
        db.connection.commit()
        # message
        flash('Usuario agregado exitosamente') 
        return redirect(url_for('usuarios_add'))
# Editar
@app.route('/edit_user/<id>')
def get_user(id):
    cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM user WHERE id = {}'. format(id))
    data = cursor.fetchall()
    return render_template('auth/user_edit.html', user = data[0])
# upgrade
@app.route('/update_user/<id>', methods = ['POST'])
def update_user(id):
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        nombre = request.form['nombre']
        rol = request.form['rol']
        movil = request.form['movil']
        domicilio = request.form['domicilio']
        password_hashed = generate_password_hash(contraseña)
        cur = db.connection.cursor()
        cur.execute( """
        UPDATE user
        SET username = %s,
            password = %s, 
            fullname = %s, 
            rol = %s, 
            t_movil = %s, 
            domicilio = %s
        WHERE id = %s
        """, (correo, password_hashed, nombre, rol, movil, domicilio, id))
        db.connection.commit()
        flash('Usuario actualizado satisfactoriamente')
        return redirect(url_for('user_list'))

@app.route('/delete_user/<string:id>')
def delete_user(id):
    cur = db.connection.cursor()
    cur.execute('DELETE FROM user WHERE id = {}'. format(id))
    db.connection.commit()
    flash('Usuario removido satisfactoriamente')    
    return redirect(url_for('usuarios_add'))

# Necesitas ayuda
@app.route('/need_help')
@login_required
def help():
    return render_template('auth/help.html')

# Captura de errores
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