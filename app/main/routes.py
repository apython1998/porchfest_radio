from app import app, db
from flask import render_template, url_for, redirect, flash, request, jsonify


@app.route('/reset_db')
def reset_db():
    pass


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')