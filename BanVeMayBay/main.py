from flask import render_template, redirect, request
from BanVeMayBay import app, login
from BanVeMayBay.models import *
from BanVeMayBay.admin import *
from flask_login import login_user
import hashlib
import hashlib


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/login-admin", methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password", "")
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        user = User.query.filter(User.username == username.strip(),
                                 User.password == password).first()
    if user:
        login_user(user=user)
    return redirect("/admin")


@app.route('/register/', methods=['GET', 'POST'])
def register():
    """Register Form"""
    if request.method == 'POST':
        new_user = User()
        new_user.username = request.form['username']
        new_user.password = hashlib.md5(request.form['password'].encode("utf-8")).hexdigest()
        new_user.first_name = request.form['first-name']
        new_user.last_name = request.form['last-name']
        new_user.active = False
        db.session.add(new_user)
        db.session.commit()
        return render_template('security/login.html')
    return render_template('register.html')


@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/booking')
def booking():
    return render_template('booking.html')


if __name__ == '__main__':
    app.run(debug=True)
