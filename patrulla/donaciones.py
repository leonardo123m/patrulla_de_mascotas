from flask import Blueprint, render_template, request, redirect, url_for, send_file
import pymysql
import io  

donac = Blueprint('donaciones', __name__)

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

#                                              PAGINAS DE DONACIONES

#  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ DONACIONES FISICAS @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@donac.route('/D_Fisicas', methods=['GET', 'POST'])
def D_Fisicas(): 
     if request.method == 'POST':
        nombre_org = request.form ['nombre_dF']
        cosas = request.form ['cosas_dF']
        razones = request.form ['razon_dF']
        lugar = request.form ['lugar_dF']
        fecha_in = request.form ['fecha_dF']
        fecha2 = request.form ['fecha2_dF']
        horario = request.form ['horario_dF']
        correo = request.form ['correo_dF']
        estado = request.form ['estado_dF']
        telefono = request.form ['tel_dF']

        if nombre_org.isdigit() or cosas.isdigit() or razones.isdigit() or lugar.isdigit():
            error_message = '''Alguno de estos campos tiene solo digitos (no valido): Nombre de la organizacion, 
                                cosas que se necesitan, razones de la donacion o lugar donde recibir la donacion'''
            print("############## El nombre de la organizacion no solo debe tener digitos ##############")
            return render_template('Donaciones/D_Fisicas.html', error=error_message)
        if not telefono.isdigit():
            error_message = "El numero de telefono no debe tener letras o caracteres diferentes a numeros"
            print("############## El numero de telefono no debe tener letras o caracteres diferentes a numeros ##############")
            return render_template('Donaciones/D_Fisicas.html', error=error_message)
        if not (correo.endswith("@gmail.com") or
                correo.endswith("@yahoo.com") or 
                correo.endswith("@outlook.com") or 
                correo.endswith("@icloud.com") or
                correo.endswith("@protonmail.com")):
            error_message = "El correo debe tener dominios validos, por ejemplo, @gmail.com"
            print("############## El correo debe tener dominios validos, por ejemplo, @gmail.com ##############")
            return render_template('Donaciones/D_Fisicas.html', error=error_message)
        

        conn = pymysql.connect(host='localhost', user='root', passwd='', db='patrulla' )
        cursor = conn.cursor()
        try:
            cursor.execute(
                '''insert into D_fisicas (
                                        nombre_dF, cosas_dF, razon_dF, lugar_dF, fecha_dF, fecha2_dF,
                                        horario_dF, correo_dF, estado_dF, tel_dF 
                                        ) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                                        ''',
                                        (nombre_org, cosas, razones, lugar,  fecha_in, fecha2, 
                                        horario, correo, estado, telefono))
            conn.commit()
            print("-----------se mandaron los datos correctamente------------------")
            mensaje = "Se mandaron los datos correctamente"
            return render_template('Donaciones/D_Fisicas.html', men=mensaje)
        except Exception as e:
            print("Error al insertar en la base de datos:", e)
            # conn.rollback() 
        finally:
            cursor.close()
            conn.close()
     return render_template('Donaciones/D_Fisicas.html')




# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ DONACIONES DE APADRINAMIENTOS @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@donac.route('/D_d_Apadrinamientos', methods=['GET', 'POST'])
def D_d_Apadrinamientos(): 
     if request.method == 'POST':
        nombre_org = request.form['nombre_dAPA']
        cosas = request.form ['cosas_dAPA']
        razones = request.form ['razon_dAPA']
        datos = request.form ['datos_dAPA']
        correo = request.form ['correo_dAPA']
        estado = request.form['estado_dAPA']
        telefono = request.form ['tel_dAPA']

        if nombre_org.isdigit():
            error_mensaje = "El campo: nombre solo tiene digitos"
            print("########## El campo: nombre solo tiene digitos  ##########")
            return render_template('Donaciones/D_d_Apadrinamientos.html', error = error_mensaje)
        if cosas.isdigit():
            error_mensaje = "El campo: cosas que quieres que te donen, no debe tener solo digitos"
            print("########## El campo: cosas que quieres que te donen, no solo debe tener digitos  ##########")
            return render_template('Donaciones/D_d_Apadrinamientos.html', error = error_mensaje)
        if razones.isdigit():
            error_mensaje = "El campo: razones por la que se piden donaciones, no debe tener solo digitos"
            print("########## El campo: razones por la que se piden donaciones, no debe tener solo digitos  ##########")
            return render_template('Donaciones/D_d_Apadrinamientos.html', error = error_mensaje)
        if datos.isdigit():
            error_mensaje = "El campo: datos de la cuenta de banco, no solo debe tener digitos"
            print("########## El campo: datos de la cuenta de banco, no solo debe tener digitos  ##########")
            return render_template('Donaciones/D_d_Apadrinamientos.html', error = error_mensaje)

        if not telefono.isdigit():
            error_mensaje = "El numero de telefono solo debe tener digitos"
            print("############### El numero de telefono solo debe tener digitos ###############")
            return render_template('Donaciones/D_d_Apadrinamientos.html', error = error_mensaje)
        if not (correo.endswith("@gmail.com") or 
                correo.endswith("@yahoo.com") or 
                correo.endswith("@outlook.com") or 
                correo.endswith("@icloud.com") or
                correo.endswith("@protonmail.com")):
            error_mensaje = "El correo debe tener un dominio valido"
            print("########## El correo debe tener un dominio valido ##########")
            return render_template('Donaciones/D_d_Apadrinamientos.html', error = error_mensaje)
            
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='patrulla' )
        cursor = conn.cursor()
        try:
            cursor.execute(
                '''insert into D_apadri (
                                        nombre_dAPA, cosas_dAPA, razon_dAPA, datos_dAPA, correo_dAPA,
                                        estado_dAPA, tel_dAPA
                                        ) values (%s,%s,%s,%s,%s,%s,%s)
                                        ''',
                                        (nombre_org, cosas, razones, datos,  correo, estado, 
                                        telefono))
            conn.commit()
            print("-----------se mandaron los datos correctamente------------------")
            mensaje = "Se mandaron los datos correctamente"
            return render_template('Donaciones/D_d_Apadrinamientos.html', men=mensaje)
        except Exception as e:
            print("Error al insertar en la base de datos:", e)
            # conn.rollback() 
        finally:
            cursor.close()
            conn.close()
     return render_template('Donaciones/D_d_Apadrinamientos.html')
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ DONACIONES MONETARIAS PARA VOLUNTARIOS @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@donac.route('/D_m_volun', methods=['GET', 'POST'])
def D_m_volun():
    if request.method == 'POST':
        nombre_org = request.form['nombre_dMON']
        razon = request.form ['razon_dMON']
        correo = request.form['correo_dMON']
        estado = request.form ['estado_dMON']
        telefono = request.form['tel_dMON']

        if nombre_org.isdigit():
            print("############### En el campo de: Nombre de la persona, no deben ir solo digitos ###############")
            error_mensaje = "En el campo de: Nombre de la persona, no deben ir solo digitos"
            return render_template('Donaciones/D_m_volun.html', error=error_mensaje)
        if razon.isdigit():
            print("############### En el campo de: Razon de donacion, no deben ir solo digitos ###############")
            error_mensaje = "En el campo de: Razon de donacion, no deben ir solo digitos"
            return render_template('Donaciones/D_m_volun.html', error=error_mensaje)
        if not (correo.endswith("@gmail.com") or 
                correo.endswith("@yahoo.com") or 
                correo.endswith("@outlook.com") or 
                correo.endswith("@icloud.com") or
                correo.endswith("@protonmail.com")):
            error_mensaje = "El correo debe tener un dominio valido"
            print("########## El correo debe tener un dominio valido ##########")
            return render_template('Donaciones/D_m_volun.html', error = error_mensaje)
        if not telefono.isdigit():
            print("############### El numero solo debe tener digitos ###############")
            error_mensaje = "El numero solo debe tener digitos"
            return render_template('Donaciones/D_m_volun.html', error=error_mensaje)
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='patrulla' )
        cursor = conn.cursor()
        try:
            cursor.execute(
                '''insert into D_m_volun (
                                        nombre_dMONV, razon_dMONV, correo_dMONV, estado_dMONV, tel_dMONV
                                        ) values (%s,%s,%s,%s,%s)
                                        ''',
                                        (nombre_org, razon, correo, estado, telefono))
            conn.commit()
            print("-----------se mandaron los datos correctamente------------------")
            mensaje = "Se mandaron los datos correctamente"
            return render_template('Donaciones/D_m_volun.html', men=mensaje)
        except Exception as e:
            print("Error al insertar en la base de datos:", e)
            # conn.rollback() 
        finally:
            cursor.close()
            conn.close()
    return render_template('Donaciones/D_m_volun.html')

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ DONACIONES MONETARIAS PARA LA COMUNIDAD @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@donac.route('/D_m_comu', methods = ['GET', 'POST'])

def D_m_comu():
    if request.method == 'POST':
        nombre_per = request.form['nombre_dMON']
        razon = request.form ['razon_dMON']
        correo = request.form ['correo_dMON']
        estado = request.form ['estado_dMON']
        telefono = request.form ['tel_dMON']

        if nombre_per.isdigit():
            print("############### El campo de nombre no deben ir solo digitos ###############")
            error_mensaje = "El campo de nombre no deben ir solo digitos"
            return render_template('Donaciones/D_m_comu.html', error = error_mensaje )
        if razon.isdigit():
            print("############### El campo de razon no deben ir solo digitos ###############")
            error_mensaje = "El campo de razon no deben ir solo digitos"
            return render_template('Donaciones/D_m_comu.html', error = error_mensaje )
        if not (correo.endswith("@gmail.com") or 
                correo.endswith("@yahoo.com") or 
                correo.endswith("@outlook.com") or 
                correo.endswith("@icloud.com") or
                correo.endswith("@protonmail.com")):
            error_mensaje = "El correo debe tener un dominio valido"
            print("########## El correo debe tener un dominio valido ##########")
            return render_template('Donaciones/D_m_comu.html', error = error_mensaje)
        if not telefono.isdigit():
            error_mensaje = "El telefono debe tener solo digitos"
            print("########## El telefono debe tener solo digitos ##########")
            return render_template('Donaciones/D_m_comu.html', error = error_mensaje)
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='patrulla' )
        cursor = conn.cursor()
        try:
            cursor.execute(
                '''insert into D_m_comu (
                                        nombre_dMON, razon_dMON, correo_dMON, estado_dMON, tel_dMON
                                        ) values (%s,%s,%s,%s,%s)
                                        ''',
                                        (nombre_per, razon, correo, estado, telefono))
            conn.commit()
            print("-----------se mandaron los datos correctamente------------------")
            mensaje = "Se mandaron los datos correctamente"
            return render_template('Donaciones/D_m_comu.html', men=mensaje)
        except Exception as e:
            print("Error al insertar en la base de datos:", e)
            # conn.rollback() 
        finally:
            cursor.close()
            conn.close()        
    return render_template('Donaciones/D_m_comu.html')
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@