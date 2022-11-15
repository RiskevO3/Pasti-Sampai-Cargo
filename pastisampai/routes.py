from flask import redirect, render_template,request,url_for,flash
from pastisampai import app,db
from pastisampai.models import User
from pastisampai.forms import RegisterForm,LoginForm
from flask_login import login_user,logout_user,login_required,current_user


username = ''

@app.route('/',methods = ["GET","POST"])
def home_page():
    if request.method == "GET":
        return render_template('index.html')

@app.route('/about',methods = ["GET","POST"])
def about_page():
    return render_template('about.html')

@app.route('/services',methods = ["GET","POST"])
def service_page():
    return render_template('service.html')

@app.route('/login',methods = ["GET","POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attemptedUser = User.query.filter_by(username=form.username.data).first()
        if attemptedUser and attemptedUser.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attemptedUser)
            flash(f"Success! sekarang kamu login sebagai {attemptedUser.username}", category='success')
            return redirect(url_for('dashboard_page'))
        else:
            flash('Username atau password salah!, harap coba kembali', category='danger')
    return render_template('login.html',form=form)

@app.route('/register',methods = ["GET","POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        userToCreate = User(username=form.username.data,fullname=form.fullname.data,email_address=form.email.data,password=form.password.data)
        db.session.add(userToCreate)
        db.session.commit()
        login_user(userToCreate)
        flash(f"Akun berhasil dibuat! sekarang kamu login sebagai {userToCreate.username}", category='success')
        return redirect(url_for('dashboard_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')


    return render_template('register.html',form=form)

@app.route('/dashboard',methods=["GET","POST"])
@login_required
def dashboard_page():# counterpart for session
    return render_template("dashboard.html")

@app.route('/customer',methods=["GET","POST"])
@login_required
def customer_page():
    return render_template('customer.html')


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))
