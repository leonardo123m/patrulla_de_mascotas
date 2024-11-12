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

veter = flask.Blueprint('veter', __name__)

@veter.route('/veterinarias_pri')
def veterinarias_pri():
    return render_template('veterinarias/veterinarias_pri.html')