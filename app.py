from distutils.command.upload import upload
from flask import Flask, render_template, request, redirect, url_for, flash
#este modulo lo vamos a usar porque nos vamos a conectar a una base de datos
from flaskext.mysql import MySQL
from datetime import datetime
import os
from flask import send_from_directory

app = Flask(__name__)
app.secret_key = "Develoteca"

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'sistema'
mysql.init_app(app)

CARPETA = os.path.join('uploads')
app.config['CARPETA'] = CARPETA

@app.route('/uploads/<nombrefoto>')
def uploads(nombrefoto):
    return send_from_directory(app.config['CARPETA'], nombrefoto)

@app.route('/')
def index():
    #una instruccion sql se va a conectar a una conexion mysql.
    sql = "select * from empleados;"
    #va ser referencia a la conexion creada (mysql.init_app(app))
    conexion = mysql.connect()
    #el cursor es informacion o donde se almacenara todo lo que se ejecuta
    cursor = conexion.cursor()
    #cuando ya se tiene el cursor se ejecuta con execute
    cursor.execute(sql)
    #para traer los datos
    empleados = cursor.fetchall()
    print (empleados)
    #aqui cerramos la instruccion
    conexion.commit()

    return render_template('empleados/index.html', empleados = empleados)

#CREAR EMPLEADO
@app.route('/create')
def create():
    return render_template('empleados/create.html')

#recibe los datos del empleado
@app.route('/store', methods=['POST'])
def storage():
    nombre = request.form['nombre']
    correo = request.form['correo']
    foto = request.files['foto']

    if nombre == '' or correo == '' or foto == '':
        flash('Recuerda llenar los datos de los campos.')
        return redirect(url_for('create'))

#PARA GUARDAR LA FOTO
    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")
    if foto.filename != '':
        nuevo_nombre_foto = tiempo + foto.filename
        foto.save("uploads/" + nuevo_nombre_foto)

    sql = "insert into empleados(id, nombre, correo, foto) values (null, %s, %s, %s);"

    datos = (nombre, correo, nuevo_nombre_foto)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()
    return redirect ('/')

#ELIMINIAR
@app.route('/borrar/<int:id>')
def borrar(id):
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("delete from empleados where id = %s", (id))
    conexion.commit()

    return redirect('/')

#EDITAR
@app.route('/editar/<int:id>')
def editar(id):
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("select * from empleados where id = %s", (id))
    empleados = cursor.fetchall()
    conexion.commit()
    print(empleados)
    return render_template ('empleados/edit.html', empleados = empleados)

@app.route('/update', methods=['POST'])
def update():
    nombre = request.form['nombre']
    correo = request.form['correo']
    foto = request.files['foto']
    id = request.form['id']

    

    sql = "update empleados set nombre=%s, correo=%s where id = %s;"

    datos = (nombre, correo, id)

    conexion = mysql.connect()
    cursor = conexion.cursor()

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")
    if foto.filename != '':
        nuevo_nombre_foto = tiempo + foto.filename
        foto.save("uploads/" + nuevo_nombre_foto)

        cursor.execute("select foto from empleados where id = %s", id)
        fila = cursor.fetchall()
        os.remove(os.path.join(app.config['CARPETA'],fila[0][0]))
        cursor.execute("update empleados set foto=%s where id=%s", (nuevo_nombre_foto, id))
        conexion.commit()
        
    cursor.execute(sql, datos)
    conexion.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(port=500, debug=True)