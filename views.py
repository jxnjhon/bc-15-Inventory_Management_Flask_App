from __init__ import app, db
from flask import render_template, url_for, request, redirect, flash
from forms import LoginForm, AssetForm
from models import *

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/super_admin_login', methods = ["GET", "POST"])
def super_admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = SuperAdmin.query.get(1)
        pswd = SuperAdmin.query.get(2)
        if str(user) == username:
            flash("Signed in successfully as {} <SuperAdmin User>".format(username))
            return redirect(request.args.get('next') or url_for('super_admin'))
        else:
            flash("{} is not a SuperAdmin User".format(username))
            return redirect(url_for('home'))
    return render_template('super_admin_login.html', form = form)


@app.route('/admin_login', methods = ["GET", "POST"])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        flash("Signed in successfully as {}  <Admin User>".format(username))
        return redirect(request.args.get('next') or url_for('admin'))
    return render_template('admin_login.html', form = form)


@app.route('/user_login', methods = ["GET", "POST"])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        flash("Signed in successfully as {} <User>".format(username))
        return redirect(request.args.get('next') or url_for('home'))
    return render_template('user_login.html', form = form)


@app.route('/super_admin', methods = ["GET", "POST"])
def super_admin():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        db.session.add(Admin(username=username, password_hash=password))
        db.session.commit()
        flash("Successfully created {} as Admin".format(username))
        return redirect(request.args.get('next') or url_for('super_admin'))
    return render_template('super_admin.html', form = form)

@app.route('/admin')
def admin():
    return render_template("admin.html")

@app.route('/admin/add_asset', methods = ["GET", "POST"])
def add_asset():
    form = AssetForm()
    if form.validate_on_submit():
        asset_name = form.asset_name.data
        description = form.description.data
        serial_no = form.serial_no.data
        serial_code = form.serial_code.data
        colour = form.colour.data
        date_bought = form.date_bought.data
        db.session.add(Assets(asset_name=asset_name, description=description,
                                serial_no=serial_no, serial_code=serial_code,
                                colour=colour, date_bought=date_bought))
        db.session.commit()
        flash("Successfully added {} to the records".format(asset_name))
        return redirect(url_for('admin'))
    return render_template('add_asset.html', form = form)

