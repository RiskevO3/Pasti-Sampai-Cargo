from flask import flash
from pastisampai import db,bcrypt,login_manager
from flask_login import UserMixin,login_user
import http.client
import json
from datetime import date
import random

# load user info from database when user login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# make relational many to many database for resi and user table
user_resi = db.Table('user_resi',db.Column('user_id',db.Integer(),db.ForeignKey('user.id')),db.Column('resi_id',db.Integer(),db.ForeignKey('resi.id')))

def validate_login(username,password):
    attemptedUser = search_user(username)
    if attemptedUser and attemptedUser.check_password_correction(attempted_password=password):
        login_user(attemptedUser)
        return(f"Success! sekarang kamu login sebagai {attemptedUser.username}", 200)
    return('Username atau password salah!, harap coba kembali', 400)


# function to create new user
def create_user(username,fullname,email_address,password,roles):
    userToCreate = User(username=username,fullname=fullname,email_address=email_address,password=password,roles=roles)
    db.session.add(userToCreate)
    db.session.commit()
    login_user(userToCreate)
    return(f"Akun berhasil dibuat! sekarang kamu login sebagai {userToCreate.username}", 200)

def create_resi(sender_n,receiver_n,origin_n,destination_n,type_of_packet,type_of_service,sender_pn,receiver_pn,weight_packet,arrived_at,ongkir):
    newResi = Resi(no_resi=generate_resi(),sender_n=sender_n,receiver_n=receiver_n,origin_n=origin_n,destination_n=destination_n,type_of_packet=type_of_packet,type_of_service=type_of_service,sender_pn=sender_pn,receiver_pn=receiver_pn,weight_packet=weight_packet,arrived_at=arrived_at,time_on_update=get_date(),time_on_deliver=get_date(),ongkir=ongkir)
    db.session.add(newResi)
    db.session.commit()
    return newResi

def create_new_order(sender_n,receiver_n,origin_n,destination_n,type_of_packet,type_of_service,sender_pn,receiver_pn,weight_packet,arrived_at,city_id,tujuan,berat):
    ongkir = create_ongkir(city_id,tujuan,berat)
    newResi = create_resi(sender_n,receiver_n,origin_n,destination_n,type_of_packet,type_of_service,sender_pn,receiver_pn,weight_packet,arrived_at,ongkir)
    return json.dumps({'no_resi':newResi.no_resi,'ongkir':ongkir})

def create_ongkir(city_id,tujuan,berat):
    kota = Kota_Ongkir.query.filter_by(city_id=city_id).first()
    return kota.cekongkir(tujuan=tujuan,berat=berat)

def create_error_messages(errors_messages,category):
    if category == 'ajax':
        l_err = []
        for err_msg in errors_messages:
            l_err.append(f'Ada kesalahan ketika membuat akun: {err_msg[0]}')
        return (l_err,400)
    elif category == 'flash':
        for err_msg in errors_messages:
            flash(f'Ada kesalahan ketika membuat akun: {err_msg[0]}')
 
def add_user_to_resi(resi,username_d,username_r):
    resi = search_noresi(int(resi))
    user_d,user_r = search_user(username_d),search_user(username_r)
    user_d.resi.append(resi)
    user_r.resi.append(resi)
    db.session.add_all([user_d,user_r])
    db.session.commit()

def update_resi(no_resi,tanggal,arrived_at):
    user = search_noresi(no_resi)
    user.time_on_update = tanggal
    user.arrived_at = arrived_at
    db.session.commit()
    return (f'success,update pada no resi {no_resi} berhasil!',200)

#function for search username
def search_user(value):
    if '@' in value:
        return User.query.filter_by(email_address=value).first()
    return User.query.filter_by(username=value).first()

def check_user(username,user_type):
    username = search_user(username)
    if not username:
        username_type = user_type
        if username_type == 'username_d':
            return (f'username untuk pengirim tidak ada!',400)
        return(f'username untuk penerima tidak ada!',400)
    return ('username terdaftar!',200)

# function for search resi from Resi table
def search_noresi(no_resi):
    resi = Resi.query.filter_by(no_resi=no_resi).first()
    if not resi:
        return ('resi tidak terdaftar!',400)
    return ('resi yang anda masukkan terdaftar!',200)

def search_city(kabKotaName):
    city = Kota.query.filter(Kota.kabkota_name.like(kabKotaName)).all()
    if city:
        l_city = []
        for citie in city:
            l_city.append(citie.to_dict())
        return (l_city,200)
    return ('Kota yang anda cari tidak ada!',400)

def track_resi(no_resi):
    noresi = search_noresi(no_resi)
    if noresi:
        data = {'arrived_at':noresi.arrived_at,'time_on_update':noresi.time_on_update}
    else:
        data = 'noresi tidak ada!'
    return (data,200)

# function for generate random resi
def generate_resi():
    resis = Resi.query.all()
    resi_list = []
    for resi in resis:
        resi_list.append(resi.no_resi)
    while True:
        random_number = random.randint(120000000,130000000)
        if random_number not in resi_list:
            return random_number

# function for get today date
def get_date():
    today = date.today()
    return today.strftime("%d/%m/%Y")

# function for get Kota_Ongkir table database for api ongkir purposes
def get_city():
    city = Kota_Ongkir.query.all()
    list_city = []
    list_city.append(('default','Pilih Kota'))
    for kota in city:
        list_city.append((kota.city_id,kota.city_name))
    return list_city

# class User model for database table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    roles = db.Column(db.String(length=30),nullable=False)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    fullname = db.Column(db.String(length=30),nullable=False)
    email_address = db.Column(db.String(length=50), nullable=False)
    password_hash = db.Column(db.String(length=60), nullable=False)
    resi = db.relationship('Resi',secondary=user_resi,backref='users')
    @property
    def password(self): 
        return self.password
    @password.setter
    def password(self, plain_text_password): #function to encrypt password when user register on this websites
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    def check_password_correction(self, attempted_password): #function to check password when user try to login.
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

# class Resi model for database table
class Resi(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    no_resi = db.Column(db.Integer(),nullable=False)
    sender_n = db.Column(db.String(length=60),nullable=False)
    receiver_n = db.Column(db.String(length=60),nullable=False)
    origin_n = db.Column(db.String(length=60),nullable=False)
    destination_n = db.Column(db.String(length=60),nullable=False)
    type_of_packet = db.Column(db.String(length=60),nullable=False)
    type_of_service = db.Column(db.String(length=60),nullable=False)
    sender_pn = db.Column(db.Integer(),nullable=False)
    receiver_pn = db.Column(db.Integer(),nullable=False)
    weight_packet = db.Column(db.String(length=30),nullable=False)
    arrived_at = db.Column(db.String(length=30),nullable=False)
    time_on_update = db.Column(db.String(length=60),nullable=False)
    time_on_deliver = db.Column(db.String(length=60),nullable=False)
    ongkir = db.Column(db.String(length=30),nullable=False)

# class Kota model for database table
class Kota(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    cabang_name = db.Column(db.String(length=30),nullable=False)
    kabkota_name = db.Column(db.String(length=30),nullable=False)
    address = db.Column(db.String(length=60),nullable=False)
    kodePos = db.Column(db.String(length=30),nullable=False)
    def to_dict(self): #function to return all of the kota model to dictionary
        return {'address':self.address,'kabkota_name':self.kabkota_name,'kodePos':self.kodePos,'cabang_name':self.cabang_name}

# class Kota_Ongkir model for database table
class Kota_Ongkir(db.Model):
    id =db.Column(db.Integer(),primary_key=True)
    city_id = db.Column(db.String(length=30),nullable=False)
    city_name = db.Column(db.String(length=30),nullable=False)
    def cekongkir(self,tujuan,berat): #cek ongkir function
        berat = berat * 1000
        conn = http.client.HTTPSConnection("api.rajaongkir.com")
        payload = f"origin={self.city_id}&destination={tujuan}&weight={berat}&courier=jne"
        headers = {
            'key': "dbe89046a22f2b3bf24a714d31d8554f",
            'content-type': "application/x-www-form-urlencoded"
            }
        conn.request("POST", "/starter/cost", payload, headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data.decode("utf-8"))
        print(tujuan)
        print(data)
        if not data['rajaongkir']['results'][0]['costs']:
            data = data['rajaongkir']['results'][0]['costs'][0]['cost'][0]['value']
            return data
        return 10000*(berat/1000)



# b = User(username='bbb',roles='user',fullname='bbb',email_address='bbb',password='bbb')
# e = User(username='eee',roles='user',fullname='eee',email_address='eee',password='eee')
# c = Resi(no_resi=120223212,sender_n='sumanto',receiver_n='sutrisno',origin_n='jl.bojongsoang',destination_n='jl.kantor baru',type_of_packet='baju',type_of_service='reguler',sender_pn=628123,receiver_pn=62847221,weight_packet='2.4kg',arrived_at='bali',time_on_update='12.44 selasa 16/11/22',time_on_deliver='16/11/22',ongkir='12000')
# d = Resi(no_resi=120223213,sender_n='sutrisno',receiver_n='habibi',origin_n='jl.sedrisna',destination_n='jl.kertajaya',type_of_packet='baju',type_of_service='reguler',sender_pn=628123,receiver_pn=62847221,weight_packet='2.4kg',arrived_at='bali',time_on_update='12.44 selasa 16/11/22',time_on_deliver='16/11/22',ongkir='12000')
