from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session, send_file
from flask_socketio import emit
from extensiones import socketio  # Importa socketio desde extensiones
from conexion import conectar
import io
import flask

chats = Blueprint('chats', __name__)

usuarios_conectados = {}

@socketio.on('connect')
def conectarsocket():
    print('Intentando conectar...')
    usuario = session.get('nom_us')
    if usuario:
        usuarios_conectados[usuario] = request.sid
        print(f'Usuario {usuario} conectado con ID {request.sid}')

@socketio.on('envmsg')
def msgenv(data):
    mensaje = data['mensaje']
    usuario = session.get('nom_us')
    print(f'mensaje, {usuario} {data}')
    emit('nuevo mensaje', {'mensaje': mensaje, 'usuario': usuario}, broadcast=True)




@chats.route('/chatgeneral')
def chatgeneral():
    nom_us = session.get('nom_us')
    return render_template('chats/chats.html', nom_us = nom_us)

@chats.route('/usuarios')
def obtener_usuarios():
    conn = conectar()
    cursor = conn.cursor()
    nom_us = session.get('nom_us')
    cursor.execute('SELECT nombre FROM cuenta WHERE nombre != %s', (nom_us,))
    print(nom_us)

    usuarios = cursor.fetchall()
    return render_template('chats/lista_usuarios.html', usuarios=usuarios)



@chats.route('/foto/<destinatario>')
def obtener_fotous(destinatario):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT foto FROM cuenta WHERE nombre=%s', (destinatario))
    foto = cursor.fetchone()
    cursor.close()
    conn.close()
    if foto and foto [0]:
        return send_file(io.BytesIO(foto[0]), mimetype = 'image/jpeg')
    else:
        return 'error al encontrar la foto', 404
    



@chats.route('/mensajes/<destinatario>')
def obtener_mensajes(destinatario):
    conn=conectar()
    cursor=conn.cursor()
    cursor.execute('select remitente, mensaje, timestamp from mensajes_privados where (remitente=%s and destinatario=%s) or (remitente=%s and destinatario=%s) order by timestamp', (session['nom_us'], destinatario, destinatario, session['nom_us']))
    mensajes=cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('chats/chatpriv.html', mensajes=mensajes, destinatario=destinatario)


@socketio.on('envmsgpriv')
def msgpriv(data):
    mensajepriv = data['mensajepriv']
    remitente = session.get('nom_us')
    destinatario = data['destinatario']

    def obtener_socket_destinatario(destinatario):
        return usuarios_conectados.get(destinatario)

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('insert into mensajes_privados (remitente, mensaje, destinatario) values(%s, %s, %s)', (remitente, mensajepriv, destinatario))
    conn.commit()
    cursor.close()
    conn.close()

    destinatario_socket_id = obtener_socket_destinatario(destinatario)

    emit('nuevo mensaje privado', {'mensaje': mensajepriv, 'remitente': remitente}, room=destinatario_socket_id)




@socketio.on('disconnect')
def disconnect():
    usuario = session.get('nom_us')
    if usuario in usuarios_conectados:
        del usuarios_conectados[usuario]
        print(f'Usuario {usuario} desconectado')

#     pip install Flask Flask-SocketIO
#     pip install eventlet
#     pip install gevent
#     pip install gevent-websocket
#     pip install flask-socketio==5.3.1
#     pip install python-socketio==5.0.2

