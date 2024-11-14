from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask import send_file, Blueprint
from werkzeug.security import check_password_hash
import flask
import pymysql
import io
import pdfkit
import jinja2
from pathlib import Path
from conexion import conectar
import gevent
import os

from admin import admin_bp 
from forms import forms
from donaciones import donac
from ajustes import ajustes
from chats import chats
from extensiones import socketio 
from veterinarias import veter
from inserts_vet import inserts
app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = "clave secreta aqui"

# Registro de los blueprints
app.register_blueprint(forms)
app.register_blueprint(admin_bp)
app.register_blueprint(donac)         
app.register_blueprint(ajustes)
app.register_blueprint(chats)
app.register_blueprint(veter)
app.register_blueprint(inserts)

socketio.init_app(app) 



# aqui hiba lo del administrador
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      
#                                                       LOGIN PROGRAMADO
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']  
        contraseña = request.form['contraseña']
        print("----------------------------------se recibieron los datos------------------------")
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='patrulla' )
        cursor = conn.cursor()
        try:
            cursor.execute('select id_usuario, email, contraseña, nombre from cuenta where email = %s and contraseña =  %s', (email, contraseña))

            user = cursor.fetchone()
            if user and user[1] == "AdministradorPDM@gmail.com": 
                if user[2] == "adminpdm15102024!!5":  # Aquí debes validar si la contraseña es correcta
                    print("@@@@@@@@@@@@@@@@@ Se capturó el admin correctamente @@@@@@@@@@@@@@@@@")
                    print(f"Email: {user[1]}, Contraseña: {user[2]}")
                return redirect(url_for('admin_bp.menu_admin')) 


            
            if user and user[2] == contraseña:  
                print("############################### login exitoso #####################")
                session['id_usuario'] = user[0] 
                print(f"ID de usuario almacenado en sesion: {session['id_usuario']}") 
                session ['nom_us'] = user[3]
                print(f"Nombre de usuario: {session['nom_us']}")
                return redirect(url_for('inicio'))

            else:
                mensaje_err = "Email o contraseña incorrectos"
                print("###################### Email o contraseña incorrectos ##############################")
                return render_template('paginas_usuario/login.html', error = mensaje_err, email = email, contraseña = contraseña)
        except Exception as e:
            print("Error al iniciar sesion", e)
            error_log = "Error al iniciar sesion", e
            return render_template('paginas_usuario/login.html', error = error_log)
        
        finally:
            cursor.close()
            conn.close()
            


    return render_template('paginas_usuario/login.html')

@app.route('/profile')
def profile():
    return render_template("profile.html")


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  PAGINA PARA CREAR CUENTA @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@app.route('/crear_cuenta', methods=['GET', 'POST'])
def crear_cuent():
  
    if request.method == 'POST':
        #NOTA: request.form sirve solo para texto, por lo tanto no se usa para mandar fotos
        nombre = request.form['nombre']
        edad = request.form['edad']
        telefono = request.form ['tel_us']
        pais = request.form['pais']
        estado = request.form['estado']
        email = request.form['email']
        contraseña = request.form['contraseña']
        caracteres_especiales = "!@#$%^&*(),.?\":{}|<>" #Para verificar si la contraseña tiene caracteres especiales

        if 'foto' in request.files and request.files['foto'].filename:
            foto = request.files['foto'].read()
            print("############################## Si selecciono una foto ######################")        
        else:
            error_message = "No se agrego una foto"
            print("##### No hay foto #####")
            return render_template('paginas_usuario/crear_cuenta.html', error=error_message, nombre = nombre, 
                                   email = email, edad = edad, telefono = telefono, pais = pais, 
                                   estado = estado, contraseña = contraseña)
        
        if foto:
            if len(foto) > 2 * 1024 * 1024:  # Maximo 2mb de almacenamiento
                error_message = "La foto de perfil no debe exceder los 2 MB."
                print("##### Foto muy grande #####")
                return render_template('paginas_usuario/crear_cuenta.html', error=error_message)

            # Validacion del tipo MIME para asegurar que sea una imagen y no un archivo cualquiera
            if not request.files['foto'].content_type.startswith('image/'):
                error_message = "El archivo debe ser una imagen: (jpg, png, jiff.)"
                print("##### Tipo de archivo no válido #####")
                return render_template('paginas_usuario/crear_cuenta.html', error=error_message)
       
        if not telefono.isdigit():
            error_message = "En el numero de telefono, solo deben ir digitos"
            tel_err = True
            print("#####  En el numero de telefono, solo deben ir digitos  #####")
            return render_template('paginas_usuario/crear_cuenta.html' , error=error_message, nombre = nombre, email = email, 
                                   edad = edad, telefono = telefono, pais = pais, estado = estado, contraseña = contraseña, tel_err = tel_err  )
        
        if len(nombre) < 6 or len(nombre) > 25:
            error_message = "El nombre debe tener minimo 6 caracteres y maximo 25 caracteres"
            nom_err = True
            print("#####  Nombre no valido  #####")
            return render_template('paginas_usuario/crear_cuenta.html' , error=error_message, nombre = nombre,
                                    email = email, edad = edad, telefono = telefono, pais = pais, estado = estado, 
                                    contraseña = contraseña, nom_err = nom_err)
        
        if nombre.isdigit(): # Verifica si en el nombre solo se pusieron numeros
            error_message = "El nombre no debe tener solo numeros"
            nom_err = True
            print("##### El nombre no debe tener solo numeros #####")
            return render_template('paginas_usuario/crear_cuenta.html' , error=error_message, nombre = nombre, 
                                   email = email, edad = edad, telefono = telefono, pais = pais, estado = estado, 
                                   contraseña = contraseña,  nom_err = nom_err)
        
        if len(contraseña) < 10 or len(contraseña) > 20: #Verifica si la contraseña tiene minimo 10 caracteres y maximo 20 caracteres
            error_message = "La contraseña debe tener minimo 10 caracteres y maximo 20 caracteres"
            cont_err = True
            print("#####  Nombre no valido  #####")
            return render_template('paginas_usuario/crear_cuenta.html' , error=error_message, nombre = nombre, 
                                   email = email, edad = edad, telefono = telefono, pais = pais, 
                                   estado = estado, contraseña = contraseña, cont_err = cont_err)
        
        if not any(char in caracteres_especiales for char in contraseña): #Verifica si la contraseña tiene caracteres especiales
            error_message = "La contraseña no tiene caracteres especiales"
            cont_err = True
            print("#####  La contraseña no tiene caracteres especiales  #####")
            return render_template('paginas_usuario/crear_cuenta.html', error=error_message, nombre = nombre, 
                                   email = email, edad = edad, telefono = telefono, pais = pais, estado = estado, 
                                   contraseña = contraseña, cont_err = cont_err)
        
        #validar finalizacion del correo electronico (@ejemplo.com), con diferentes dominios, con ayuda 
        # del ".endswitch(valor con el que se quiere finalizar)"
        if not (
            email.endswith("@gmail.com") or 
            email.endswith("@yahoo.com") or 
            email.endswith("@outlook.com") or
            email.endswith("@icloud.com") or 
            email.endswith("@protonmail.com")
            ):
            error_message = "El correo debe terminar con un dominio valido, por ejemplo @gmail.com"
            em_err = True
            print("#####  El correo debe terminar con un dominio valido #####")
            return render_template('paginas_usuario/crear_cuenta.html', error=error_message, nombre = nombre, 
                                   email = email, edad = edad, telefono = telefono, pais = pais, estado = estado, 
                                   contraseña = contraseña, em_err = em_err)
        
        #Hace conexion con la bd para ver si el correo ya existe
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='patrulla' )
        cursor = conn.cursor()
        cursor.execute('SELECT nombre FROM cuenta WHERE  nombre = %s', ( nombre,))
        user = cursor.fetchone()
        cursor.execute('SELECT  email FROM cuenta WHERE email = %s ', (email,))
        user2 = cursor.fetchone()
        if user :
            error_message = "El nombre ya esta en uso, pruebe con uno unico."
            nom_err = True
            print("##### El nombre ya esta en uso, pruebe con uno unico. #####")
            return render_template('paginas_usuario/crear_cuenta.html', error=error_message, nombre = nombre, 
                                   email = email, edad = edad, telefono = telefono, pais = pais, estado = estado, 
                                   contraseña = contraseña, nom_err = nom_err)
        if user2 :
            error_message = "El email ya esta en uso, pruebe con uno unico."
            em_err = True
            print("##### El email ya esta en uso, pruebe con uno unico. #####")
            return render_template('paginas_usuario/crear_cuenta.html', error=error_message, nombre = nombre, 
                                   email = email, edad = edad, telefono = telefono, pais = pais, estado = estado, 
                                   contraseña = contraseña, em_err = em_err)
        
        
        
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='patrulla' )
        cursor = conn.cursor()
        try:
            cursor.execute('''insert into cuenta (nombre, edad, tel_us, pais, estado, email,
                            contraseña, foto) 
                            values (%s, %s, %s, %s, %s, %s, %s, %s)''', 
                            (nombre, edad, telefono,  pais, estado, email, contraseña, foto))
            conn.commit()
            print("--------------Se a creado la cuenta correctamente y se a dirigido a la pagina de inicio-----------------------------")
           
            cursor.execute('SELECT id_usuario from cuenta where email = %s ', (email,))
            datos = cursor.fetchone()
            if datos:
                session['id_usuario'] = datos[0] 
                print(f"ID de usuario almacenado en creacion de cuenta: {session['id_usuario']}") 
            else:
                print("No se puedo obtener el id del usuario")
            
            return redirect(url_for('inicio'))  
          
        except Exception as e:
            conn.rollback() 
            error_message = f"Error al insertar cuenta en la base de datos: {str(e)}"

            print("Error al insertar en la base de datos:", e)
            return render_template('paginas_usuario/crear_cuenta.html', error=error_message)

        finally:
            cursor.close()
            conn.close()

    return render_template('paginas_usuario/crear_cuenta.html')



 #   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ PAGINA PARA VER INFORMACION DEL PERFIL @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@app.route('/info_cuenta')
def info_cuenta():
    id_usuario = session.get('id_usuario')#Buscamos usuario por medio del id 
    if not id_usuario:# si no se encurntra el usuario, manda un print (que no serviria de nada xd)
        print("-------------------------------Usuario no encontrado----------------------")
        return "Usuario no autenticado", 403  
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='patrulla')
    cursor = conn.cursor()
    cursor.execute('SELECT nombre, edad, tel_us, pais, estado, email, id_usuario  FROM cuenta WHERE id_usuario = %s', (id_usuario,))
    datos = cursor.fetchall() 
    conn.close()
    if datos:   #Verificamos que tengamos los datos antes de pasarlos a la plantilla
        print("************ Si tiene datos ***********")
        return render_template("paginas_usuario/info_cuenta.html", dts=datos)
    else:
        print("No se encontraron datos para el usuario", 404)
        return "No se encontraron datos para el usuario", 404
   

   #aqui van los formularios

    

#  +++++++++++++++++++++++++++++++++++++++++++++ LAYOUT NAVEGADOR  +++++++++++++++++++++++++++++++++++++++++++++
@app.route('/layout')
def layout():
    id_usuario = session.get('id_usuario')#extrae el id del usuario
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='patrulla')
    cursor = conn.cursor()
    cursor.execute('SELECT foto FROM cuenta WHERE id_usuario = %s', (id_usuario,))
    foto = cursor.fetchone() #busca su foto de perfil por medio del id
 
    conn.close()
    if foto and foto[0]:  # Verifica que haya foto
        return send_file(io.BytesIO(foto[0]), mimetype='image/jpeg')  # Cambia el MIME type si es necesario
    else:
        return "Imagen no encontrada", 404


@app.route('/inicio')
def inicio():
    id_usuario = session.get('id_usuario')
    return render_template("paginas_usuario/inicio.html", dts = id_usuario )



@app.route('/sus_reportes')
def sus_reportes():
    return render_template("paginas_usuario/sus_reportes.html")

@app.route('/info_adop_us')
def info_adop_us():
    id_usuario = session.get('id_usuario')
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='patrulla')
    cursor = conn.cursor()
    cursor.execute('''select id_adop, id_de_us, nombre_ad, direccion_ad, 
                   estado_ad,telefono_ad, correo_ad, nombre_mad, tip_ad, raza_ad,
                   edad_ad, alto_ad, longitud_ad, color_ad, 
                   sexo_ad, desc_ad FROM FormMascAdop WHERE id_de_us = %s''', (id_usuario,))
    
    dato  = cursor.fetchall()
    session['id_adop'] = dato[0] 
    print(f"ID del formulario: {session['id_adop']}")
    conn.close()
    return render_template("paginas_de_reportes/info_adop_us.html", dts = dato, id = id_usuario)



@app.route('/foto_report/<string:id>')
def foto_report(id):
    # id_adop = session.get('id_adop')
    try:
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='patrulla')
        cursor = conn.cursor()
        
        cursor.execute('''SELECT foto_ad FROM FormMascAdop WHERE 
                       id_adop = %s''' , (id,))
        foto = cursor.fetchone()
        
        if foto is None:
            return "No se encontró el registro con ese ID", 404
        
      
        
        if foto and foto[0]:  # Verifica que haya foto
            print("Imagen encontrada de usuarios adopcion ")
            return send_file(io.BytesIO(foto[0]), mimetype='image/jpeg')
        else:
            return "Imagen no encontrada", 404
    except Exception as e:
        return f"Error: {e}", 500
    finally:
        conn.close()  # Asegúrate de cerrar la conexión en caso de error

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ EDITAR CUENTA @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ---------- extraer imagen

@app.route('/foto_perf/<string:id>')
def foto_perf(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='patrulla')
    cursor = conn.cursor()
    cursor.execute('SELECT foto FROM cuenta WHERE id_usuario = %s', (id,))
    foto = cursor.fetchone()
    conn.close()
    if foto and foto[0]:  # Verifica que haya foto
        return send_file(io.BytesIO(foto[0]), mimetype='image/jpeg')  # Cambia el MIME type si es necesario
    else:
        return "Imagen no encontrada", 404
# ----------
@app.route('/editar_perfil')
def editar_perfil():
    id_usuario = session.get('id_usuario')
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='patrulla')
    cursor = conn.cursor()
    cursor.execute('''SELECT id_usuario, nombre FROM cuenta WHERE id_usuario = %s''', (id_usuario,))
    dato  = cursor.fetchone()
    conn.close()
    if dato is None:
        return "Usuario no encontrado", 404 
    return render_template('paginas_usuario/editar_perfil.html', com=dato)


@app.route('/editar_perf/<string:id>', methods=['GET', 'POST'])
def editar_perf(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
       

        conn = pymysql.connect(host='localhost', user='root', passwd='', db='patrulla')
        cursor = conn.cursor()
        cursor.execute('''UPDATE cuenta SET nombre = %s WHERE id_usuario = %s''', 
                           (nombre, id))
        conn.commit()
        conn.close()
    return redirect(url_for('info_cuenta') )

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ BORRAR CUENTA @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@app.route('/borrar_perfil')
def borrar_perfil():
    # id_usuario = session.get('id_usuario')
    # conn = pymysql.connect(host='localhost', user='root', passwd='', db='patrulla')
    # cursor = conn.cursor()
    # cursor.execute('DELETE FROM cuenta WHERE id_usuario = %s', (id_usuario,))
    # cursor.execute('DELETE FROM formmascadop where id_de_us = %s', (id_usuario,))
    # conn.commit()
    # conn.close()
    # print("Id de cuenta eliminada:"+ id_usuario)
    return render_template('paginas_usuario/borrar_perfil.html')
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Editar datos personales @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@app.route('/logeo_verificacion', methods=['GET', 'POST'])
def logeo_verificacion():
    if request.method == 'POST':
      
        contraseña = request.form['contraseña']
        print("----------------------------------se recibieron los datos------------------------")
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='patrulla' )
        cursor = conn.cursor()



    
        try:
            cursor.execute('select id_usuario, email, contraseña from cuenta where  contraseña =  %s', (contraseña))

            user = cursor.fetchone()
            if user and user[2] == contraseña:  
                print("############################### Verificacion exitosa #####################")
                return redirect(url_for('editar_dtsper'))

            else:
                mensaje_err = "Contraseña incorrecta"
                print("###################### Contraseña incorrecta al querer editar perfil ##############################")
                return render_template('Ajustes/logeo_verificacion.html', error = mensaje_err, contraseña = contraseña)
        except Exception as e:
            print("Error al entrar para editar perfil", e)
            error_log = "Error al entrar para editar perfil", e
            return render_template('paginas_usuario/login.html', error = error_log)
        
        finally:
            cursor.close()
            conn.close()
    return render_template('Ajustes/logeo_verificacion.html')
#********* EDITAR 

    # return render_template('Ajustes/editar_dtsper.html')
@app.route('/editar_dtsper')
def editar_dtsper():
    id_usuario = session.get('id_usuario')
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='patrulla')
    cursor = conn.cursor()
    cursor.execute('''SELECT id_usuario, tel_us, edad, contraseña, email FROM cuenta WHERE id_usuario = %s''', (id_usuario,))
    dato  = cursor.fetchone()
    conn.close()
    if dato is None:
        return "Usuario no encontrado", 404 
    return render_template('Ajustes/editar_dtsper.html', com=dato)

@app.route('/editar_dtsperd/<string:id>', methods=['GET', 'POST'])
def editar_dtsperd(id):
    if request.method == 'POST':
        edad = request.form['edad']
        telefono = request.form['telefono']
        contraseña = request.form['contraseña']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='patrulla')
        cursor = conn.cursor()
        try:
            cursor.execute('''UPDATE cuenta SET edad = %s, tel_us = %s, contraseña = %s WHERE id_usuario = %s''', 
                            (edad,telefono,contraseña, id))
            conn.commit()
            print("@@@@@@@@@@@@@@@@@@@ Se actualizo el usuario @@@@@@@@@@@@@@@@@@@@@")
            men = "Se actualizaron tus datos"
        except:
            print("error al actualizar el perfil")
        finally:
            conn.close()
    return render_template('Ajustes/ajustes_principal.html',  mensaje=men)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ CERRAR SESION @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @app.route('/logout', methods=['POST'])
# def logout():
#     print("sessions antes", +session)
#     session.clear()
#     print("Datos de sesión después de cerrar sesión:", session)
#     response = redirect(url_for('login'))
#     response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
#     response.headers['Pragma'] = 'no-cache'
#     response.headers['Expires'] = '-1'
#     return response




#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


# http://127.0.0.1:5500  para ir rápido y solo copiar y pegar xdxd
if __name__ == "__main__":
    socketio.run(app, host='127.0.0.1', port=5500, debug=True)
    #app.run(host='127.0.0.1', port=5500, debug=True)


#     @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
#     choco install wkhtmltopdf
#     pip install pdfkit