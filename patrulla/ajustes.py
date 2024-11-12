from flask import Blueprint, render_template, request, redirect, url_for, send_file, session
import pymysql
import io  
ajustes = Blueprint('ajustes', __name__)


@ajustes.route('/principal')
def principal():
    return render_template('Ajustes/ajustes_principal.html')

@ajustes.route('/cerrar_sesion')
def cerrar_sesion():
    session.pop('id_usuario')
    session.pop('nom_us')
    session.clear()
    logout = "Ha cerrado sesion"
    return render_template('paginas_usuario/login.html', logout = logout)