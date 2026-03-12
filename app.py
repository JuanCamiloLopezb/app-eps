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

# --- 1. MENÚ PRINCIPAL ---
@app.route('/')
def index():
    return render_template('index.html')

# --- 2. REGISTRO DE PACIENTE ---
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

# --- 3. REGISTRO DE CITA MÉDICA ---
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
            cursor.close()
            conexion.close()
        return redirect(url_for('registro_cita'))
    
    return render_template('registro_cita.html')

# --- 4. CONSULTA CON INNER JOIN ---
@app.route('/consulta_cita', methods=['GET', 'POST'])
def consulta_cita():
    if request.method == 'POST':
        doc = request.form['documento']
        
        conexion = conectar_db()
        cursor = conexion.cursor(dictionary=True)
        try:
            sql = """
            SELECT citas.id, pacientes.nombre, pacientes.apellido, citas.medico, 
                   citas.tipo_cita, citas.fecha, citas.hora, citas.direccion_eps 
            FROM pacientes 
            INNER JOIN citas ON pacientes.documento = citas.documento 
            WHERE pacientes.documento = %s
            """
            cursor.execute(sql, (doc,))
            resultados = cursor.fetchall()
            
            if resultados:
                return render_template('resultado_cita.html', datos=resultados)
            else:
                flash('No se encontraron citas para este número de documento.')
        except Exception as e:
            flash(f'Error al consultar: {e}')
        finally:
            cursor.close()
            conexion.close()
            
    return render_template('consulta_cita.html')

# --- 5. EDITAR CITA MÉDICA ---
@app.route('/editar_cita/<int:id>', methods=['GET', 'POST'])
def editar_cita(id):
    conexion = conectar_db()
    cursor = conexion.cursor(dictionary=True)
    
    if request.method == 'POST':
        nuevo_medico = request.form['medico']
        nueva_fecha = request.form['fecha']
        nueva_hora = request.form['hora']
        
        try:
            sql = "UPDATE citas SET medico = %s, fecha = %s, hora = %s WHERE id = %s"
            cursor.execute(sql, (nuevo_medico, nueva_fecha, nueva_hora, id))
            conexion.commit()
            flash('¡La cita médica fue actualizada correctamente!')
            return redirect(url_for('consulta_cita'))
        except Exception as e:
            flash(f'Error al actualizar la cita: {e}')
        finally:
            cursor.close()
            conexion.close()
            
    else:
        try:
            cursor.execute("SELECT * FROM citas WHERE id = %s", (id,))
            cita = cursor.fetchone()
            return render_template('editar_cita.html', cita=cita)
        except Exception as e:
            flash(f'Error al cargar la cita: {e}')
            return redirect(url_for('consulta_cita'))
        finally:
            cursor.close()
            conexion.close()

if __name__ == '__main__':
    app.run(debug=True, port=5001)