from flask import redirect, render_template,request,url_for,flash,session,jsonify
from pastisampai import app,db
from pastisampai.models import User,Resi,Kota,Kota_Ongkir,get_date,generate_resi,search_noresi
from pastisampai.forms import RegisterForm,LoginForm,dropPointForm,checkResiForm,updateResiForm,addNewOrder,addUsername
from flask_login import login_user,logout_user,login_required,current_user
import json

@app.route('/',methods = ["GET","POST"])
def home_page():
    if request.method == "GET":
        return render_template('index.html')

@app.route('/about',methods = ["GET","POST"])
def about_page():
    form = dropPointForm()
    if form.validate_on_submit():
        kabkotaName = f'%{form.searchCity.data}%'
        city = Kota.query.filter(Kota.kabkota_name.like(kabkotaName)).all()
        if city:
            l_city = []
            for citie in city:
                l_city.append(citie.to_dict())
            return (l_city,200)
        return ('Kota yang anda cari tidak ada!',400)
    return render_template('about.html',form=form)

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
            return redirect(url_for('account_info'))
        else:
            flash('Username atau password salah!, harap coba kembali', category='danger')
    return render_template('login.html',form=form)

@app.route('/register',methods = ["GET","POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        userToCreate = User(username=form.username.data,fullname=form.fullname.data,email_address=form.email.data,password=form.password.data,roles='user')
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
    user = current_user.resi
    return render_template("dashboard.html",resis=user)

@app.route('/account_info',methods=["GET","POST"])
@login_required
def account_info():
    return render_template('account_info.html')


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))



@app.route('/admin_dashboard',methods=['GET','POST'])
@login_required
def dashboard_admin_page():
    if current_user.roles == 'admin':
        form = addNewOrder()
        if form.validate_on_submit():
            kota = Kota_Ongkir.query.filter_by(city_id=form.kota_asal.data).first()
            ongkir = kota.cekongkir(tujuan=form.kota_tujuan.data,berat=int(form.weight_packet.data))
            newResi = Resi(no_resi=generate_resi(),sender_n=form.sender_n.data,receiver_n=form.receiver_n.data,origin_n=form.origin_n.data,destination_n=form.destination_n.data,type_of_packet=form.type_of_packet.data,type_of_service=form.type_of_service.data,sender_pn=form.sender_pn.data,receiver_pn=form.receiver_pn.data,weight_packet=form.weight_packet.data,arrived_at=form.origin_n.data,time_on_update=get_date(),time_on_deliver=get_date(),ongkir=ongkir)
            db.session.add(newResi)
            db.session.commit()
            data = json.dumps({'no_resi':newResi.no_resi,'ongkir':ongkir})
            session['data'] = data
            return redirect(url_for('confirm_page',data=data))
        return render_template('add.html',form=form)
    flash('Youre not and admin!',category='danger')
    return redirect(url_for('account_info'))

@app.route('/confirm',methods=['GET','POST'])
@login_required
def confirm_page():
    form = addUsername()
    if request.method =='GET':
        if 'data' in session:
            data = request.args['data']
            data = session['data']
            data = json.loads(data)
            return render_template('confirm.html',data=data,form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            resi = search_noresi(int(form.no_resi.data))
            user_d = User.query.filter_by(username=form.username_d.data).first()
            user_r = User.query.filter_by(username=form.username_r.data).first()
            user_d.resi.append(resi)
            user_r.resi.append(resi)
            db.session.add_all([user_d,user_r])
            db.session.commit()
            del session['data']
            return(f'tambah resi dengan nomor {form.no_resi.data} sukses!',200)
        if form.errors != {}:
            l_err = []
            for err_msg in form.errors.values():
                l_err.append(f'There was an error with searching a resi: {err_msg}')
            return (l_err,400)
    flash('you cant access this page directly!',category='danger')
    return redirect(url_for('home_page'))

@app.route('/check_username',methods=['POST'])
@login_required
def check_username():
    if current_user.roles == 'admin':
        username = User.query.filter_by(username=request.form.get('username')).first()
        if not username:
            username_type = request.form.get('type_username')
            if username_type == 'username_d':
                return (f'username untuk pengirim tidak ada!',400)
            return(f'username untuk penerima tidak ada!',400)
        return ('username terdaftar!',200)

@app.route('/update',methods=['POST','GET'])
@login_required
def update_page():
    if current_user.roles == 'admin':
        form = updateResiForm()
        if form.validate_on_submit():
            user = search_noresi(form.noresi.data)
            user.time_on_update = form.tanggal.data
            user.arrived_at = form.arrived_at.data
            db.session.commit()
            return (f'success,update pada no resi {form.noresi.data} berhasil!',200)
        if form.errors != {}:
            l_err = []
            for err_msg in form.errors.values():
                l_err.append(f'There was an error with searching a resi: {err_msg}')
            return(l_err,400)
        return render_template('update.html',form=form)
    flash('Youre not and admin!',category='danger')
    return redirect(url_for('account_info'))


@app.route('/tracking',methods = ["GET","POST"])
@login_required
def tracking_page():
    if current_user.roles == 'admin':
        form = checkResiForm()
        if form.validate_on_submit():
            noresi = search_noresi(form.noresi.data)
            if noresi:
                data = {'arrived_at':noresi.arrived_at,'time_on_update':noresi.time_on_update}
            else:
                data = 'noresi tidak ada!'
            return (data,200)
        return render_template('tracking.html',form=form)
    flash('Youre not and admin!',category='danger')
    return redirect(url_for('account_info'))


@app.route('/cekresi',methods=['POST'])
@login_required
def cek_resi():
    if current_user.roles == 'admin':
        resi = search_noresi(int(request.form.get('resi')))
        if not resi:
            return ('resi tidak terdaftar!',400)
        return ('berhasil',200)
    return 400

