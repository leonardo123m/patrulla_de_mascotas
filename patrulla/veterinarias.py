from flask import Flask , session, render_template, request, redirect, url_for, flash
from flask import send_file
from flask import Blueprint
from werkzeug.security import check_password_hash
import flask
import pymysql
import io
import pdfkit
import jinja2
import jsonify
from pathlib import Path
import os
from inserts_vet import insertar_veterinarias 
veter = flask.Blueprint('veter', __name__)




@veter.route('/veterinarias_pri')
def veterinarias_pri():
    insertar_veterinarias()
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='patrulla')
    cursor = conn.cursor()
    cursor.execute('''SELECT id_veterinaria ,latitud, longitud from veterinarias''')
    datos = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return render_template('veterinarias/veterinarias_pri.html', dts = datos)

