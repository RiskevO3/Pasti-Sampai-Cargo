from flask import redirect, render_template,request,url_for,flash,session,jsonify
from pastisampai import app,db
from pastisampai.models import search_noresi,search_user,search_city,create_user,create_resi,create_ongkir
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
        city = search_city(kabKotaName=f'%{form.searchCity.data}%')
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
    if not current_user.is_authenticated:
        form = LoginForm()
        if form.validate_on_submit():
            attemptedUser = search_user(form.username.data)
            if attemptedUser and attemptedUser.check_password_correction(attempted_password=form.password.data):
                login_user(attemptedUser)
                return(f"Success! sekarang kamu login sebagai {attemptedUser.username}", 200)
            return('Username atau password salah!, harap coba kembali', 400)
        return render_template('login.html',form=form)
    flash(f'You have been signed in as {current_user.username}',category='info')
    return redirect(url_for('account_info'))

@app.route('/register',methods = ["GET","POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        userToCreate = create_user(username=form.username.data,fullname=form.fullname.data,email_address=form.email.data,password=form.password.data,roles='user')
        login_user(userToCreate)
        return(f"Akun berhasil dibuat! sekarang kamu login sebagai {userToCreate.username}", 200)
    if form.errors != {}: #If there are not errors from the validations
        l_err = []
        for err_msg in form.errors.values():
            l_err.append(f'Ada kesalahan ketika membuat akun: {err_msg[0]}')
        return (l_err,400)
    return render_template('register.html',form=form)


@app.route('/account_info',methods=["GET","POST"])
@login_required
def account_info():
    return render_template('account_info.html')

@app.route('/dashboard',methods=["GET","POST"])
@login_required
def dashboard_page():# counterpart for session
    user = current_user.resi
    return render_template("dashboard.html",resis=user)

@app.route('/admin_dashboard',methods=['GET','POST'])
@login_required
def dashboard_admin_page():
    if current_user.roles == 'admin':
        form = addNewOrder()
        if form.validate_on_submit():
            ongkir = create_ongkir(city_id=form.kota_asal.data,tujuan=form.kota_tujuan.data,berat=int(form.weight_packet.data))
            newResi = create_resi(sender_n=form.sender_n.data,receiver_n=form.receiver_n.data,origin_n=form.origin_n.data,destination_n=form.destination_n.data,type_of_packet=form.type_of_packet.data,type_of_service=form.type_of_service.data,sender_pn=form.sender_pn.data,receiver_pn=form.receiver_pn.data,weight_packet=form.weight_packet.data,arrived_at=form.origin_n.data,ongkir=ongkir)
            data = json.dumps({'no_resi':newResi.no_resi,'ongkir':ongkir})
            session['data'] = data
            return redirect(url_for('confirm_page',data=data))
        return render_template('add.html',form=form)
    flash('Youre not and admin!',category='error')
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
            user_d,user_r = search_user(form.username_d.data),search_user(form.username_r.data)
            user_d.resi.append(resi)
            user_r.resi.append(resi)
            db.session.add_all([user_d,user_r])
            db.session.commit()
            del session['data']
            return(f'tambah resi dengan nomor {form.no_resi.data} sukses!',200)
        if form.errors != {}:
            l_err = []
            for err_msg in form.errors.values():
                l_err.append(f'There was an error when adding a resi: {err_msg[0]}')
            return (l_err,400)
    flash('you cant access this page directly!',category='error')
    return redirect(url_for('home_page'))

# routes for update resi from database
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
                l_err.append(f'There was an error with searching a resi: {err_msg[0]}')
            return(l_err,400)
        return render_template('update.html',form=form)
    flash('Youre not and admin!',category='error')
    return redirect(url_for('account_info'))

# routes for tracking from database
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
    flash('Youre not and admin!',category='error')
    return redirect(url_for('account_info'))

# routes for check no_resi from database
@app.route('/cekresi',methods=['POST'])
@login_required
def cek_resi():
    if current_user.roles == 'admin':
        resi = search_noresi(int(request.form.get('resi')))
        if not resi:
            return ('resi tidak terdaftar!',400)
        return ('resi yang anda masukkan terdaftar!',200)
    return 400

# routes for check username on database
@app.route('/check_username',methods=['POST'])
@login_required
def check_username():
    if current_user.roles == 'admin':
        username = search_user(request.form.get('username'))
        if not username:
            username_type = request.form.get('type_username')
            if username_type == 'username_d':
                return (f'username untuk pengirim tidak ada!',400)
            return(f'username untuk penerima tidak ada!',400)
        return ('username terdaftar!',200)

# logout routes to logout user
@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!",category='info')
    return redirect(url_for("home_page"))

