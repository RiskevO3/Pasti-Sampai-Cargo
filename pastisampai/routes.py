from flask import redirect, render_template,request,url_for,flash,session
from pastisampai import app,db
from pastisampai.models import search_noresi,search_city,create_user,add_user_to_resi,validate_login,create_error_messages,update_resi,track_resi,check_user,create_new_order
from pastisampai.forms import RegisterForm,LoginForm,dropPointForm,checkResiForm,updateResiForm,addNewOrder,addUsername
from flask_login import logout_user,login_required,current_user
import json


@app.errorhandler(404)
def page_not_found(e):
    flash('this page is doesnt exist!',category='error')
    if 'url' in session:
        return redirect(session['url'])
    return redirect(url_for('home_page'))


@app.route('/',methods = ["GET"])
def home_page():
    if request.method == "GET":
        session['url'] = url_for('home_page')
        return render_template('index.html')

@app.route('/about',methods = ["GET","POST"])
def about_page():
    session['url'] = url_for('about_page')
    form = dropPointForm()
    if form.validate_on_submit():
        return search_city(kabKotaName=f'%{form.searchCity.data}%')
    return render_template('about.html',form=form)

@app.route('/services',methods = ["GET"])
def service_page():
    session['url'] = url_for('service_page')
    return render_template('service.html')

@app.route('/login',methods = ["GET","POST"])
def login_page():
    if not current_user.is_authenticated:
        session['url'] = url_for('login_page')
        form = LoginForm()
        if form.validate_on_submit():
            return validate_login(username=form.username.data,password=form.password.data)
        return render_template('login.html',form=form)
    flash(f'You have been signed in as {current_user.username}',category='info')
    if 'url' in session:
        return redirect(session['url'])
    return redirect(url_for('home_page'))

@app.route('/register',methods = ["GET","POST"])
def register_page():
    if not current_user.is_authenticated:
        session['url'] = url_for('register_page')
        form = RegisterForm()
        if form.validate_on_submit():
            return create_user(username=form.username.data,fullname=form.fullname.data,email_address=form.email.data,password=form.password.data,roles='user')
        if form.errors != {}: #If there are not errors from the validations
            return create_error_messages(form.errors.values(),'ajax')
        return render_template('register.html',form=form)
    flash(f'You have been signed in as {current_user.username}',category='info')
    if 'url' in session:
        return redirect(session['url'])
    return redirect(url_for('home_page'))


@app.route('/account_info',methods=["GET","POST"])
@login_required
def account_info():
    session['url'] = url_for('account_info')
    return render_template('account_info.html')

@app.route('/dashboard',methods=["GET","POST"])
@login_required
def dashboard_page():
    if not current_user.roles == 'admin':
        session['url'] = url_for('dashboard_page')
        user = current_user.resi
        return render_template("dashboard.html",resis=user)
    flash('admin cant access those pages!',category='error')
    if 'url' in session:
        return redirect(session['url'])
    return redirect(url_for('home_page'))

@app.route('/admin_dashboard',methods=['GET','POST'])
@login_required
def dashboard_admin_page():
    if current_user.roles == 'admin':
        session['url'] = url_for('dashboard_admin_page')
        form = addNewOrder()
        if form.validate_on_submit():
            data = create_new_order(city_id=form.kota_asal.data,tujuan=form.kota_tujuan.data,berat=int(form.weight_packet.data),sender_n=form.sender_n.data,receiver_n=form.receiver_n.data,origin_n=form.origin_n.data,destination_n=form.destination_n.data,type_of_packet=form.type_of_packet.data,type_of_service=form.type_of_service.data,sender_pn=form.sender_pn.data,receiver_pn=form.receiver_pn.data,weight_packet=form.weight_packet.data,arrived_at=form.origin_n.data)
            session['data'] = data
            return redirect(url_for('confirm_page',data=data))
        if form.errors != {}:
            create_error_messages(form.errors.values(),'flash')
        return render_template('add.html',form=form)
    flash('Youre not and admin!',category='error')
    if 'url' in session:
        return redirect(session['url'])
    return redirect(url_for('home_page'))

@app.route('/confirm',methods=['GET','POST'])
@login_required
def confirm_page():
    form = addUsername()
    if request.method =='GET':
        if 'data' in session:
            session['url'] = url_for('confirm_page')
            data = session['data']
            data = json.loads(data)
            return render_template('confirm.html',data=data,form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            add_user_to_resi(resi=form.no_resi.data,username_d=form.username_d.data,username_r=form.username_r.data)
            del session['data']
            return(f'tambah resi dengan nomor {form.no_resi.data} sukses!',200)
        if form.errors != {}:
            return create_error_messages(form.errors.values(),'ajax')
    if 'url' in session:
        return redirect(session['url'])
    return redirect(url_for('home_page'))

# routes for update resi from database
@app.route('/update',methods=['POST','GET'])
@login_required
def update_page():
    if current_user.roles == 'admin':
        session['url'] = url_for('update_page')
        form = updateResiForm()
        if form.validate_on_submit():
            return update_resi(no_resi=form.noresi.data,tanggal=form.tanggal.data,arrived_at=form.arrived_at.data)
        if form.errors != {}:
            return create_error_messages(form.errors.values(),'ajax')
        return render_template('update.html',form=form)
    flash('Youre not and admin!',category='error')
    if 'url' in session:
        return redirect(session['url'])
    return redirect(url_for('home_page'))

# routes for tracking from database
@app.route('/tracking',methods = ["GET","POST"])
@login_required
def tracking_page():
    if current_user.roles == 'admin':
        session['url'] = url_for('tracking_page')
        form = checkResiForm()
        if form.validate_on_submit():
            return track_resi(no_resi=form.noresi.data)
        return render_template('tracking.html',form=form)
    flash('Youre not and admin!',category='error')
    if 'url' in session:
        return redirect(session['url'])
    return redirect(url_for('home_page'))

# routes for check no_resi from database
@app.route('/cekresi',methods=['POST'])
@login_required
def cek_resi():
    if current_user.roles == 'admin':
        return search_noresi(int(request.form.get('resi')))
    return 400

# routes for check username on database
@app.route('/check_username',methods=['POST'])
@login_required
def check_username():
    if current_user.roles == 'admin':
        return check_user(username=request.form.get('username'),user_type=request.form.get('type_username'))
    
# logout routes to logout user
@app.route('/logout',methods=['POST'])
def logout_page():
    logout_user()
    return({"messages":"You have been logged out!","url":url_for('home_page')},200)

