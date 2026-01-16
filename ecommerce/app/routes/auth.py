import logging

from flask import Blueprint, request, jsonify, render_template, redirect
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User
from app import limiter

auth = Blueprint('auth', __name__)

@auth.route('/browser/register', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def register_browser():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User(
            email=email,
            password_hash=generate_password_hash(password)
        )

        logging.info('Writing to DB...')
        db.session.add(user)
        db.session.commit()
        logging.info('Done writing.')

        return redirect('/browser/login')
    return render_template('register.html')

@auth.route('/register', methods=['POST'])
@limiter.limit("5 per minute")
def register():
    data = request.get_json()
    if 'email' not in data or 'password' not in data:
        return jsonify({'message': 'Error: both email and password required'}), 400

    user = User(
        email=data['email'],
        password_hash=generate_password_hash(data['password'])
    )

    logging.info('Writing to DB...')
    db.session.add(user)
    db.session.commit()
    logging.info('Done writing.')

    return jsonify({'message': 'User created'}), 201

@auth.route('/browser/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login_browser():
    if request.method == 'POST':
        logging.info('Querying DB...')
        user = User.query.filter_by(email=request.form['email']).first()
        logging.info('Done querying.')

        if user and check_password_hash(user.password_hash, request.form['password']):
            login_user(user)
            return redirect('/')
        
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    data = request.get_json()

    logging.info('Querying DB...')
    user = User.query.filter_by(email=data['email']).first()
    logging.info('Done querying.')

    if user and check_password_hash(user.password_hash, data['password']):
        login_user(user)
        return jsonify({'message': 'Logged in'})

    return jsonify({'message': 'Invalid credentials'}), 401

@auth.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({'message': 'Logged out'})