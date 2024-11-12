from flask import Blueprint, render_template, request, redirect, url_for, send_file
import pymysql
import io
import flask

# Crear un Blueprint para las rutas de administración
admin_bp = Blueprint('admin_bp', __name__)


# Rutas de administrador
@admin_bp.route('/Admin')
def Admin():
    return render_template('layouts/Admin.html')

@admin_bp.route('/menu_admin')
def menu_admin():
    return render_template('Administrador/Menu_admin.html')

@admin_bp.route('/cuentas', methods=['GET', 'POST'])
def cuentas():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='patrulla')
    cursor = conn.cursor()
    cursor2 = conn.cursor()

    if request.method == 'POST':
        pais = request.form['pais']
        estado = request.form['estado']
    try:
        cursor.execute('''SELECT id_usuario, nombre, edad, tel_us, pais, estado,
                        email, contraseña, foto, fecha_creacion FROM 
                       cuenta where id_usuario >= 2 and pais = %s and estado = %s 
                       ORDER BY id_usuario''', (pais,estado,))
        datos = cursor.fetchall()


        cursor2.execute('''select COUNT(id_usuario) from cuenta where pais = %s and estado = %s 
                       ORDER BY id_usuario''', (pais,estado,))
        datos2 = cursor2.fetchone()
        total_cuentas = datos2[0]




        print("se obtubieron las cuentas para el admin de estado: "+estado)
        print("cantidad de cuentas por Estado:"+ str(total_cuentas))
      
        t = totalcuent()
        mensaje = "Cuentas de "+ estado 
        return render_template('Administrador/buscar_cuentas.html', usu=datos, m=mensaje, 
                               totalc=total_cuentas, tot = t)
    
    except:
        error = "Hubo un error al buscar las cuentas"
        print("Hubo un error al buscar las cuentas")
        return render_template('Administrador/buscar_cuentas.html', er = error)
    finally:
        conn.close()
        
       

def totalcuent():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='patrulla')
    cursor3 = conn.cursor()

    try:
        cursor3.execute('SELECT COUNT(id_usuario) FROM cuenta')
        datos3 = cursor3.fetchone()
        totaltodas = datos3[0]
        print("Cantidad de todas las cuentas: " + str(totaltodas))
        return totaltodas
    except Exception as e:
        print(f"Error al obtener el total de cuentas: {str(e)}")
        return 0  # En caso de error, devolvemos 0 como resultado
    finally:
        conn.close()






@admin_bp.route('/foto/<int:id_usuario>')
def obtener_foto(id_usuario):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='patrulla')
    cursor = conn.cursor()
    cursor.execute('SELECT foto FROM cuenta WHERE id_usuario = %s', (id_usuario,))
    foto = cursor.fetchone()
    conn.close()
    if foto and foto[0]:  # Verifica que haya foto
        return send_file(io.BytesIO(foto[0]), mimetype='image/jpeg')  # Cambia el MIME type si es necesario
    else:
        return "Imagen no encontrada", 404

@admin_bp.route('/editar_cuenta/<string:id>')
def editar_cuenta(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='patrulla')
    cursor = conn.cursor()
    cursor.execute('''SELECT id_usuario, nombre, edad, tel_us, pais, estado, email,
                      contraseña, foto, fecha_creacion FROM cuenta WHERE id_usuario = %s''', (id,))
    dato  = cursor.fetchone()
    conn.close()
    if dato is None:
        return "Usuario no encontrado", 404 
    return render_template('Administrador/Editar_cuenta.html', com=dato)

@admin_bp.route('/editar_usu/<string:id>', methods=['GET', 'POST'])
def editar_usu(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        edad = request.form['edad']
        telefono = request.form['tel_us']
        pais = request.form['pais']
        estado = request.form['estado']
        email = request.form['email']

        conn = pymysql.connect(host='localhost', user='root', passwd='', db='patrulla')
        cursor = conn.cursor()
        cursor.execute('''UPDATE cuenta SET nombre = %s, edad = %s, 
                           tel_us = %s, pais = %s, estado = %s, 
                           email = %s WHERE id_usuario = %s''', 
                           (nombre, edad, telefono, pais, estado, email, id))
        conn.commit()
        conn.close()
    return redirect(url_for('admin_bp.todas_cuentas'))

@admin_bp.route('/eliminar_cuenta/<string:id>')
def eliminar_cuenta(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='patrulla')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cuenta WHERE id_usuario = %s', (id,))
    cursor.execute('DELETE FROM formmascadop where id_de_us = %s', (id,))
    conn.commit()
    conn.close()
    print("Id de cuenta eliminada:"+ id)
    return render_template('Administrador/Cuentas.html')


@admin_bp.route('/cuenta_completa/<int:id>')
def cuenta_completa(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='patrulla')
    cursor = conn.cursor()
    cursor.execute('''SELECT id_usuario, nombre, edad, tel_us, pais, estado, email,
                      contraseña, foto, fecha_creacion FROM cuenta WHERE id_usuario = %s''', (id,))
    dato  = cursor.fetchone()
    conn.close()
    if dato is None:
        return "Usuario no encontrado", 404 
    
    return render_template('Administrador/cuenta_completa.html', com=dato)

@admin_bp.route('/todas_cuentas')
def todas_cuentas():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='patrulla')
    cursor = conn.cursor()
    cursor2 =conn.cursor()

    cursor.execute('''SELECT id_usuario, nombre, email, edad FROM cuenta where id_usuario >= 2''')
    dato  = cursor.fetchall()
  

    cursor2.execute('SELECT COUNT(id_usuario) FROM cuenta')
    datos2 = cursor2.fetchone()
    totaltodas = datos2[0]
    conn.close()
    print("Cantidad de todas las cuentas: " + str(totaltodas))

    if not dato:
        return "Usuario no encontrado", 404 
    
    return render_template('Administrador/Cuentas.html', usu=dato, t=totaltodas)
