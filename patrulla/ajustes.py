from flask import Blueprint, render_template, request, redirect, url_for, send_file
import pymysql
import io  
ajustes = Blueprint('ajustes', __name__)


@ajustes.route('/principal')
def principal():
    return render_template('Ajustes/ajustes_principal.html')