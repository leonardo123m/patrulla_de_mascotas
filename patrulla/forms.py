from flask import Flask , session, render_template, request, redirect, url_for, flash
from flask import send_file
from flask import Blueprint
from werkzeug.security import check_password_hash
import flask
import pymysql
import io
import pdfkit
import jinja2
from pathlib import Path
import os

forms = flask.Blueprint('forms', __name__)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#------------------------------------------------------PAGINA PARA PUBLICAR MASCOTA PERDIDA -------------------------------------
@forms.route('/Buscar_m_perdida', methods=['GET', 'POST'])
def buscar_m_perdida():
    if request.method == 'POST': #extrae los campos del formulario (son muchos xdxd)
        #INFORMACION DEL DUEÑO
        nombre = request.form['nombre_due']
        direccion = request.form['direccion_due']
        telefono = request.form['telefono_due']
        correo = request.form['correo_due']
        #INFORMACION DE LA MASCOTA
        nombre_masc = request.form['nombre_masc']
        tipo_masc = request.form['tip_masc']
        raza_masc = request.form['raza_masc']
        edad_masc = request.form['edad_masc']
        alto = request.form['alto_masc']
        longitud_masc = request.form['longitud_masc']
        color_masc = request.form['color_masc']
        sexo_masc = request.form['sexo_masc']
        descripcion = request.form['desc_masc']
        #INFORMACION DE LA PERDIDA
        fecha = request.form['fecha_per']
        estado = request.form['estado_per']
        lugar = request.form['lugar_masc']
        hora = request.form['hora_masc']#diferente
        circuns = request.form['cir_masc']
        #INFORMACION ADICIONAL
        if 'foto_masc' in request.files and request.files['foto_masc'].filename:#Se valida si se agrego una foto o no
            foto = request.files['foto_masc'].read()
            print("############################## Si selecciono una foto ######################")        
        else:
            error_message = "No se agrego una foto"
            print("##### No hay foto #####")
            return render_template('paginas_de_reportes/Buscar_m_perdida.html', error=error_message)
        collar = request.form['collar_per']
        
        if not telefono.isdigit():
            error_message = "El telefono solo debe tener numeros"
            print ("######################  En el telefono solo debe tener numeros ######################")
            return render_template('paginas_de_reportes/Buscar_m_perdida.html', error=error_message)

        if not (correo.endswith("@gmail.com")  or
                correo.endswith("@yahoo.com") or
                correo.endswith("@outlook.com") or
                correo.endswith("@icloud.com") or
                correo.endswith("@protonmail.com")):
            error_message = "El correo debe terminar con un dominio valido, por ejemplo @gmail.com"
            print ("######################  El dominio debe tener un dominio corrrecto ######################")
            return render_template('paginas_de_reportes/Buscar_m_perdida.html', error=error_message)
        
        if foto:#Validacion del tipo de dato de la imagen y que no pase de los 2mb 
                if len(foto) > 2 * 1024 * 1024:  # Maximo 2mb de almacenamiento
                    error_message = "La foto de la mascota  no debe exceder los 2 MB."
                    print("##### Foto muy grande #####")
                    return render_template('paginas_de_reportes/Buscar_m_perdida.html', error=error_message)

                # Validacion del tipo MIME para asegurar que sea una imagen y no un archivo cualquiera
                if not request.files['foto_masc'].content_type.startswith('image/'):
                    error_message = "El archivo debe ser una imagen: (jpg, png, etc.)"
                    print("##### Tipo de archivo no válido #####")
                    return render_template('paginas_de_reportes/Buscar_m_perdida.html', error=error_message)
        
        
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='patrulla' )
        cursor = conn.cursor()
        try:
            cursor.execute(
                '''insert into B_ma_perdida (
                                                nombre_due, direccion_due, telefono_due, correo_due, nombre_masc, 
                                                tip_masc, raza_masc, edad_masc, alto_masc, longitud_masc, color_masc, 
                                                sexo_masc, desc_masc, fecha_per, estado_per, lugar_masc, hora_masc,
                                                cir_masc, foto_masc, collar_per
                                                ) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                                            ''',
                                    (nombre, direccion, telefono, correo, nombre_masc, tipo_masc, raza_masc, edad_masc, 
                                    alto, longitud_masc, color_masc, sexo_masc, descripcion, fecha, estado, lugar, 
                                    hora, circuns, foto, collar))
            conn.commit()
            print("-----------se mandaron los datos correctamente------------------")
            mensaje = "Se mandaron los datos correctamente"
            return render_template('paginas_de_reportes/Buscar_m_perdida.html', men=mensaje)
        except Exception as e:
            print("Error al insertar en la base de datos:", e)
            # conn.rollback() 
        finally:
            cursor.close()
            conn.close()

        try:
            print("Preparando para crear el PDF")
            ruta_template = Path(forms.root_path, 'templates', 'template.html')
            info = {
                "nombredue": nombre,#
                "direcciondue": direccion,#
                "telefonodue": telefono,#
                "correodue": correo,#
                "nombremasc": nombre_masc,#
                "tipomasc": tipo_masc,#
                "razamasc": raza_masc,#
                "edadmasc": edad_masc,
                "longitud": longitud_masc,
                "alto": alto,
                "colormasc": color_masc,#
                "sexomasc": sexo_masc,#
                "descmasc": descripcion,#
                "fechaper": fecha,
                "estadoper": estado,#
                "lugarmasc": lugar,#
                "horamasc": hora,#
                "cirmasc": circuns,
                "fotomasc": foto,#
                "collarper": collar,
                "url_for": url_for
            }
      
            crea_pdf(str(ruta_template), info)

        except Exception as e:
            print(f"Error al crear el PDF: {e}")
    return render_template('paginas_de_reportes/Buscar_m_perdida.html')

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  PAGINA PARA REGISTRAR MASCOTA PARA SER ADOPTADA   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@forms.route('/Mascotas_e_adopcion', methods=['GET', 'POST'])
def Mascotas_e_adopcion():    
     id_usuario = session.get('id_usuario')
     accion = None  
     if request.method == 'POST':
       accion = request.form['accion']
       if accion == 'Publicar':
        #INFORMACION DE LA PERSONA
        nombre = request.form['nombre_ad']
        direccion = request.form ['direccion_ad']
        estado = request.form['estado_ad']
        telefono = request.form['telefono_ad']
        correo = request.form['correo_ad']
        #INFORMACION DE LA MASCOTA
        nombre_mad = request.form['nombre_mad']
        tip_ad = request.form['tip_ad']
        raza_ad = request.form['raza_ad']
        edad_ad = request.form['edad_ad']
        alto_ad = request.form['alto_ad']
        longitud_ad = request.form ['longitud_ad']
        color_ad = request.form ['color_ad']
        sexo_ad = request.form['sexo_ad']
        desc_ad = request.form['desc_ad']
        print("Campos ingresados")
 
        if not telefono.isdigit():
            tel_err = True
            error_message = "El telefono debe ser digito"
            print("######################### El telefono debe ser digito #########################")
            return render_template('paginas_de_reportes/Mascotas_e_adopcion.html', error=error_message, nombre = nombre,
                                   direccion = direccion, estado = estado, telefono = telefono, correo = correo, 
                                    nombre_mad = nombre_mad, tip_ad = tip_ad, raza_ad = raza_ad, edad_ad = edad_ad,
                                      alto_ad = alto_ad, longitud_ad = longitud_ad, color_ad = color_ad,
                                        sexo_ad = sexo_ad, desc_ad = desc_ad, tel_err = tel_err)
        
        if nombre.isdigit():
            error_message = "El nombre no debe ser solo digito"
            nom_err = True
            print("######################### El nombre no debe ser solo digito #########################")
            return render_template('paginas_de_reportes/Mascotas_e_adopcion.html', error=error_message, nombre = nombre,
                                   direccion = direccion, estado = estado, telefono = telefono, correo = correo, 
                                    nombre_mad = nombre_mad, tip_ad = tip_ad, raza_ad = raza_ad, edad_ad = edad_ad,
                                      alto_ad = alto_ad, longitud_ad = longitud_ad, color_ad = color_ad,
                                        sexo_ad = sexo_ad, desc_ad = desc_ad, nom_err = nom_err)
        if direccion.isdigit():
            error_message = "La direccion no debe ser solo digito"
            dir_err = True
            print("######################### La direccion no debe ser solo digito #########################")
            return render_template('paginas_de_reportes/Mascotas_e_adopcion.html', error=error_message, nombre = nombre,
                                   direccion = direccion, estado = estado, telefono = telefono, correo = correo, 
                                    nombre_mad = nombre_mad, tip_ad = tip_ad, raza_ad = raza_ad, edad_ad = edad_ad,
                                      alto_ad = alto_ad, longitud_ad = longitud_ad, color_ad = color_ad,
                                        sexo_ad = sexo_ad, desc_ad = desc_ad, dir_err = dir_err)
        if not (correo.endswith("@gmail.com") or 
                correo.endswith("@yahoo.com") or 
                correo.endswith("@outlook.com") or 
                correo.endswith("@icloud.com") or
                correo.endswith("@protonmail.com")):
            em_err =True
            error_message = "El correo debe terminar con un dominio valido, por ejemplo: @gmail.com, etc"
            print("######################### Dominio del correo no valido #########################")
            return render_template('paginas_de_reportes/Mascotas_e_adopcion.html', error=error_message, nombre = nombre,
                                   direccion = direccion, estado = estado, telefono = telefono, correo = correo, 
                                    nombre_mad = nombre_mad, tip_ad = tip_ad, raza_ad = raza_ad, edad_ad = edad_ad,
                                      alto_ad = alto_ad, longitud_ad = longitud_ad, color_ad = color_ad,
                                        sexo_ad = sexo_ad, desc_ad = desc_ad, em_err = em_err)
        #VALIDACION DE FOTO
        if 'foto_ad' in request.files and request.files['foto_ad'].filename:#Se valida si se agrego una foto o no
            foto = request.files['foto_ad'].read()
            print("############################## Si selecciono una foto ######################")        
        else:
            error_message = "No se agrego una foto"
            foto_er = True
            print("######################### No hay foto #########################")
            return render_template('paginas_de_reportes/Mascotas_e_adopcion.html', error=error_message, nombre = nombre,
                                   direccion = direccion, estado = estado, telefono = telefono, correo = correo, 
                                    nombre_mad = nombre_mad, tip_ad = tip_ad, raza_ad = raza_ad, edad_ad = edad_ad,
                                      alto_ad = alto_ad, longitud_ad = longitud_ad, color_ad = color_ad,
                                        sexo_ad = sexo_ad, desc_ad = desc_ad, foto_er = foto_er)
        
        if foto:#Validacion del tipo de dato de la imagen y que no pase de los 2mb 
                if len(foto) > 2 * 1024 * 1024:  # Maximo 2mb de almacenamiento
                    error_message = "La foto de la mascota  no debe exceder los 2 MB."
                    print("##### Foto muy grande #####")
                    foto_er = True
                    return render_template('paginas_de_reportes/Mascotas_e_adopcion.html', error=error_message, nombre = nombre,
                                   direccion = direccion, estado = estado, telefono = telefono, correo = correo, 
                                    nombre_mad = nombre_mad, tip_ad = tip_ad, raza_ad = raza_ad, edad_ad = edad_ad,
                                      alto_ad = alto_ad, longitud_ad = longitud_ad, color_ad = color_ad,
                                        sexo_ad = sexo_ad, desc_ad = desc_ad, foto_er = foto_er)

                # Validacion del tipo MIME para asegurar que sea una imagen y no un archivo cualquiera
                if not request.files['foto_ad'].content_type.startswith('image/'):
                    error_message = "El archivo debe ser una imagen: (jpg, png, jiff.)"
                    print("##### Tipo de archivo no válido #####")
                    foto_er = True
                    return render_template('paginas_de_reportes/Mascotas_e_adopcion.html', error=error_message, nombre = nombre,
                                   direccion = direccion, estado = estado, telefono = telefono, correo = correo, 
                                    nombre_mad = nombre_mad, tip_ad = tip_ad, raza_ad = raza_ad, edad_ad = edad_ad,
                                      alto_ad = alto_ad, longitud_ad = longitud_ad, color_ad = color_ad,
                                        sexo_ad = sexo_ad, desc_ad = desc_ad, foto_er = foto_er)
        
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='patrulla' )
        cursor = conn.cursor()
        try:
            cursor.execute(
                '''insert into FormMascAdop (
                                    nombre_ad, direccion_ad, estado_ad, telefono_ad, 
                                    correo_ad, nombre_mad, tip_ad, raza_ad, edad_ad,
                                    alto_ad,  longitud_ad, color_ad, sexo_ad, desc_ad,
                                    foto_ad, id_de_us
                                    ) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                                ''',
                            (nombre, direccion, estado,telefono, correo, nombre_mad, tip_ad,
                            raza_ad, edad_ad, alto_ad, longitud_ad, color_ad, sexo_ad, desc_ad, foto, id_usuario, ))
            conn.commit()
            
            print(f"ID de usuario almacenado en el formulario para dar en adopcion: {session['id_usuario']}") 

            print("-----------se mandaron los datos correctamente------------------")
            mensaje = "Se mandaron los datos correctamente"
            return render_template('paginas_de_reportes/Mascotas_e_adopcion.html', men=mensaje)
        except Exception as e:
            print("Error al insertar en la base de datos:", e)
            # conn.rollback() 
        finally:
            cursor.close()
            conn.close()
     if accion == 'Crear pdf':
            return "presiono crear pdf"
     if accion == 'Crear pdf y publicar':
            #INFORMACION DE LA PERSONA
        nombre = request.form['nombre_ad']
        direccion = request.form ['direccion_ad']
        estado = request.form['estado_ad']
        telefono = request.form['telefono_ad']
        correo = request.form['correo_ad']
        #INFORMACION DE LA MASCOTA
        nombre_mad = request.form['nombre_mad']
        tip_ad = request.form['tip_ad']
        raza_ad = request.form['raza_ad']
        edad_ad = request.form['edad_ad']
        alto_ad = request.form['alto_ad']
        longitud_ad = request.form ['longitud_ad']
        color_ad = request.form ['color_ad']
        sexo_ad = request.form['sexo_ad']
        desc_ad = request.form['desc_ad']
        print("Campos ingresados")
 
        if not telefono.isdigit():
            tel_err = True
            error_message = "El telefono debe ser digito"
            print("######################### El telefono debe ser digito #########################")
            return render_template('paginas_de_reportes/Mascotas_e_adopcion.html', error=error_message, nombre = nombre,
                                   direccion = direccion, estado = estado, telefono = telefono, correo = correo, 
                                    nombre_mad = nombre_mad, tip_ad = tip_ad, raza_ad = raza_ad, edad_ad = edad_ad,
                                      alto_ad = alto_ad, longitud_ad = longitud_ad, color_ad = color_ad,
                                        sexo_ad = sexo_ad, desc_ad = desc_ad, tel_err = tel_err)
        
        if nombre.isdigit():
            error_message = "El nombre no debe ser solo digito"
            nom_err = True
            print("######################### El nombre no debe ser solo digito #########################")
            return render_template('paginas_de_reportes/Mascotas_e_adopcion.html', error=error_message, nombre = nombre,
                                   direccion = direccion, estado = estado, telefono = telefono, correo = correo, 
                                    nombre_mad = nombre_mad, tip_ad = tip_ad, raza_ad = raza_ad, edad_ad = edad_ad,
                                      alto_ad = alto_ad, longitud_ad = longitud_ad, color_ad = color_ad,
                                        sexo_ad = sexo_ad, desc_ad = desc_ad, nom_err = nom_err)
        if direccion.isdigit():
            error_message = "La direccion no debe ser solo digito"
            dir_err = True
            print("######################### La direccion no debe ser solo digito #########################")
            return render_template('paginas_de_reportes/Mascotas_e_adopcion.html', error=error_message, nombre = nombre,
                                   direccion = direccion, estado = estado, telefono = telefono, correo = correo, 
                                    nombre_mad = nombre_mad, tip_ad = tip_ad, raza_ad = raza_ad, edad_ad = edad_ad,
                                      alto_ad = alto_ad, longitud_ad = longitud_ad, color_ad = color_ad,
                                        sexo_ad = sexo_ad, desc_ad = desc_ad, dir_err = dir_err)
        if not (correo.endswith("@gmail.com") or 
                correo.endswith("@yahoo.com") or 
                correo.endswith("@outlook.com") or 
                correo.endswith("@icloud.com") or
                correo.endswith("@protonmail.com")):
            em_err =True
            error_message = "El correo debe terminar con un dominio valido, por ejemplo: @gmail.com, etc"
            print("######################### Dominio del correo no valido #########################")
            return render_template('paginas_de_reportes/Mascotas_e_adopcion.html', error=error_message, nombre = nombre,
                                   direccion = direccion, estado = estado, telefono = telefono, correo = correo, 
                                    nombre_mad = nombre_mad, tip_ad = tip_ad, raza_ad = raza_ad, edad_ad = edad_ad,
                                      alto_ad = alto_ad, longitud_ad = longitud_ad, color_ad = color_ad,
                                        sexo_ad = sexo_ad, desc_ad = desc_ad, em_err = em_err)
        #VALIDACION DE FOTO
        if 'foto_ad' in request.files and request.files['foto_ad'].filename:#Se valida si se agrego una foto o no
            foto = request.files['foto_ad'].read()
            print("############################## Si selecciono una foto ######################")        
        else:
            error_message = "No se agrego una foto"
            foto_er = True
            print("######################### No hay foto #########################")
            return render_template('paginas_de_reportes/Mascotas_e_adopcion.html', error=error_message, nombre = nombre,
                                   direccion = direccion, estado = estado, telefono = telefono, correo = correo, 
                                    nombre_mad = nombre_mad, tip_ad = tip_ad, raza_ad = raza_ad, edad_ad = edad_ad,
                                      alto_ad = alto_ad, longitud_ad = longitud_ad, color_ad = color_ad,
                                        sexo_ad = sexo_ad, desc_ad = desc_ad, foto_er = foto_er)
        
        if foto:#Validacion del tipo de dato de la imagen y que no pase de los 2mb 
                if len(foto) > 2 * 1024 * 1024:  # Maximo 2mb de almacenamiento
                    error_message = "La foto de la mascota  no debe exceder los 2 MB."
                    print("##### Foto muy grande #####")
                    foto_er = True
                    return render_template('paginas_de_reportes/Mascotas_e_adopcion.html', error=error_message, nombre = nombre,
                                   direccion = direccion, estado = estado, telefono = telefono, correo = correo, 
                                    nombre_mad = nombre_mad, tip_ad = tip_ad, raza_ad = raza_ad, edad_ad = edad_ad,
                                      alto_ad = alto_ad, longitud_ad = longitud_ad, color_ad = color_ad,
                                        sexo_ad = sexo_ad, desc_ad = desc_ad, foto_er = foto_er)

                # Validacion del tipo MIME para asegurar que sea una imagen y no un archivo cualquiera
                if not request.files['foto_ad'].content_type.startswith('image/'):
                    error_message = "El archivo debe ser una imagen: (jpg, png, jiff.)"
                    print("##### Tipo de archivo no válido #####")
                    foto_er = True
                    return render_template('paginas_de_reportes/Mascotas_e_adopcion.html', error=error_message, nombre = nombre,
                                   direccion = direccion, estado = estado, telefono = telefono, correo = correo, 
                                    nombre_mad = nombre_mad, tip_ad = tip_ad, raza_ad = raza_ad, edad_ad = edad_ad,
                                      alto_ad = alto_ad, longitud_ad = longitud_ad, color_ad = color_ad,
                                        sexo_ad = sexo_ad, desc_ad = desc_ad, foto_er = foto_er)
        
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='patrulla' )
        cursor = conn.cursor()
        try:
            cursor.execute(
                '''insert into FormMascAdop (
                                    nombre_ad, direccion_ad, estado_ad, telefono_ad, 
                                    correo_ad, nombre_mad, tip_ad, raza_ad, edad_ad,
                                    alto_ad,  longitud_ad, color_ad, sexo_ad, desc_ad,
                                    foto_ad, id_de_us
                                    ) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                                ''',
                            (nombre, direccion, estado,telefono, correo, nombre_mad, tip_ad,
                            raza_ad, edad_ad, alto_ad, longitud_ad, color_ad, sexo_ad, desc_ad, foto, id_usuario, ))
            conn.commit()
            
            print(f"ID de usuario almacenado en el formulario para dar en adopcion: {session['id_usuario']}") 

            print("-----------se mandaron los datos correctamente------------------")
            mensaje = "Se mandaron los datos correctamente"
            return render_template('paginas_de_reportes/Mascotas_e_adopcion.html', men=mensaje)
        except Exception as e:
            print("Error al insertar en la base de datos:", e)
            # conn.rollback() 
        finally:
            cursor.close()
            conn.close()
     return render_template('paginas_de_reportes/Mascotas_e_adopcion.html')




#   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ PAGINAS PARA VER MASCOTAS EN ADOPCION Y SUS FOTOGRAFIAS @@@@@@@@@@@@@@@@@@@@@@@@@@@
@forms.route('/ver_m_adop')
def ver_m_adop():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='patrulla')
    cursor = conn.cursor()

    # Primera consulta para obtener los datos del formulario de adopción
    cursor.execute(''' SELECT id_adop, nombre_ad, direccion_ad, estado_ad, telefono_ad, correo_ad,
                        nombre_mad, tip_ad, raza_ad, edad_ad, alto_ad, longitud_ad, color_ad, sexo_ad,
                        desc_ad, foto_ad, id_de_us, fecha_creacion FROM FormMascAdop ''')

    datos = cursor.fetchall()

    datos_completos = []#Despues de obtener los datos se crea una lista para almacenar el nombre del usuario y su 
                        #id 

    for dato in datos:
        id_de_us = dato[16]  # Extraemos el id_de_us de los datos del formulario
        
        # Hacemos consulta para obtener el nombre del usuario
        cursor.execute('SELECT nombre FROM cuenta WHERE id_usuario = %s', (id_de_us,))
        usuario = cursor.fetchone()#Extrae su informacion
        
        if usuario:
            nombre_usuario = usuario[0]
        else:
            nombre_usuario = "Desconocido" 

        datos_completos.append({
            'formulario': dato,
            'nombre_usuario': nombre_usuario
        })

        #PARA QUE LE ENTIENDAN MEJOR, ES LO MISMO QUE HACER ESTO:
        #  #numeros = [1, 2, 3]
        # numeros.appened(4)
        #print(numeros)  Salida: [1, 2, 3, 4]
    conn.close()

    # Pasamos los datos al template
    return render_template('paginas_de_reportes/ver_en_adop.html', datos_completos=datos_completos)



@forms.route('/obf/<int:id_usuario>')
def obf(id_usuario):
    try:
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='patrulla')
        cursor = conn.cursor()
        cursor.execute('SELECT foto FROM cuenta WHERE id_usuario = %s', (id_usuario,))
        foto = cursor.fetchone()

        if foto and foto[0]:  # Si existe la foto
            return send_file(io.BytesIO(foto[0]), mimetype='image/jpeg')  # Cambia el mimetype según sea necesario
        else:
            return send_file('ruta/a/imagen_predeterminada.jpg', mimetype='image/jpeg')  # Imagen predeterminada si no hay foto
    except Exception as e:
        print(f"Error: {e}")
        return '', 500
    finally:
        conn.close()


@forms.route('/obtener_f/<int:id_adop>')
def obtener_f(id_adop):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='patrulla')
    cursor = conn.cursor()
    cursor.execute('SELECT foto_ad FROM FormMascAdop WHERE id_adop = %s', (id_adop,))

    foto = cursor.fetchone()
 
    conn.close()
    if foto and foto[0]:  # Verifica que haya foto
        return send_file(io.BytesIO(foto[0]), mimetype='image/jpeg')  # Cambia el MIME type si es necesario
    else:
        return "Imagen no encontrada", 404   








#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  FUNCION DEL PDF @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def crea_pdf(ruta_template, info, ruta_css=''):
    print("Dentro de la función crea_pdf")
    ruta_template = Path(ruta_template)
    nombre_template = ruta_template.name
    ruta_template = ruta_template.parent

    print("Ruta de la plantilla:", ruta_template)
    print("Nombre de la plantilla:", nombre_template)

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(str(ruta_template)))
    template = env.get_template(nombre_template)
    html = template.render(info)
    print(html)

    options = {
        'page-size': 'Letter',
        'margin-top': '0.05in',
        'margin-right': '0.05in',
        'margin-bottom': '0.05in',
        'margin-left': '0.05in',
        'encoding': 'UTF-8',
        'enable-local-file-access': ''
    }

    config = pdfkit.configuration(wkhtmltopdf="C:/ProgramData/chocolatey/bin/wkhtmltopdf.exe")
    for i in range(1,10):
        j = 1
        ruta_salida = Path(forms.root_path, 'reconocimiento_python{}.pdf'.format(j))
        j=j+1
        i=i+0
    pdfkit.from_string(html, str(ruta_salida), css=ruta_css, options=options, configuration=config)