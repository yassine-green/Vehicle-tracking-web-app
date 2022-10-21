from crypt import methods
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Vehicle
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/home')
@login_required
def home():
    data = Vehicle.query.all()
    return render_template('home.html', vehicles = data)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('auth.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Username does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(username) < 2:
            flash('Username must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('auth.home'))

    return render_template("sign_up.html", user=current_user)


@auth.route('/admin')
@login_required
def admin():
    data = Vehicle.query.all()
    id = current_user.id
    if id == 1:
        return render_template("admin.html", vehicles = data)
    else:
        flash("You must be the Admin to access the Admin Page.")
        return redirect(url_for('login.html'))

@auth.route('/insert', methods = ['POST'])
def insert():
    from .models import Vehicle
    if request.method == 'POST':
        new_vehicle = Vehicle(reg= request.form['reg'],
        name= request.form['name'],
        brand= request.form['brand'],
        color= request.form['color'],
        seats= request.form['seats'],
        inServ= request.form['inServ'],
        outServ= request.form['outServ'])
        
        db.session.add(new_vehicle)
        db.session.commit()
        
        flash("Vehicle added successfully", category='success')
        return redirect(url_for('auth.admin'))

@auth.route('/update', methods = ['GET', 'POST'])
def update():
    from .models import Vehicle
    if request.method == 'POST':
        v_data=Vehicle.query.get(request.form.get('id'))
        
        v_data.reg = request.form['reg']
        v_data.name= request.form['name']
        v_data.brand = request.form['brand']
        v_data.color = request.form['color']
        v_data.seats = request.form['seats']
        v_data.inServ = request.form['inServ']
        v_data.outServ = request.form['outServ']

        db.session.commit()
        flash("Vehicle updated successfully", category='success')
        return redirect(url_for('auth.admin'))

@auth.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    from .models import Vehicle
    v_del=Vehicle.query.get(id)
    db.session.delete(v_del)
    db.session.commit()
    flash("Vehicle deleted successfully", category='success')
    return redirect(url_for('auth.admin'))
