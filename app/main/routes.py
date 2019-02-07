from app import db
from flask import render_template, url_for, redirect, flash, request, jsonify, current_app
from flask_login import current_user, login_required
from app.main import bp


@bp.route('/reset_db')
def reset_db():
    pass


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')