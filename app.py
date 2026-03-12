from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from config import Config

app = Flask(__name__)
app.secret_key = 'citas_medicas_sena' 

# --- CONEXIÓN A LA BASE DE DATOS ---
def conectar_db():
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB
    )

@app.route('/')
def index():
    return render_template('index.html')

# --- REGISTRO DE PACIENTE ---
@app.route('/registro_paciente', methods=['GET', 'POST'])
def registro_paciente():
    if request.method == 'POST':
        doc = request.form['documento']
        nom = request.form['nombre']
        ape = request.form['apellido']
        tel = request.form['telefono']
        cor = request.form['correo']
        eps = request.form['eps']
        
        conexion = conectar_db()
        cursor = conexion.cursor()
        try:
            sql = "INSERT INTO pacientes (documento, nombre, apellido, telefono, correo, eps) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (doc, nom, ape, tel, cor, eps))
            conexion.commit()
            flash('Paciente registrado con éxito en el sistema.')
        except Exception as e:
            flash(f'Error al registrar paciente: {e}')
        finally:
            cursor.close()
            conexion.close()
        return redirect(url_for('registro_paciente'))
    return render_template('registro_paciente.html')

# --- REGISTRO DE CITA MÉDICA ---
@app.route('/registro_cita', methods=['GET', 'POST'])
def registro_cita():
    if request.method == 'POST':
        doc = request.form['documento']
        med = request.form['medico']
        tipo = request.form['tipo_cita']
        fec = request.form['fecha']
        hor = request.form['hora']
        dir_eps = request.form['direccion_eps']
        
        conexion = conectar_db()
        cursor = conexion.cursor()
        try:
            sql = "INSERT INTO citas (documento, medico, tipo_cita, fecha, hora, direccion_eps) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (doc, med, tipo, fec, hor, dir_eps))
            conexion.commit()
            flash('Cita médica agendada correctamente.')
        except Exception as e:
            flash(f'Error al agendar cita: {e}')
        finally:
            cursor.close