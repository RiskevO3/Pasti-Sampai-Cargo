from pastisampai import db,bcrypt,login_manager
from flask_login import UserMixin
import http.client
import json
from datetime import date
import random

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def generate_resi():
    resis = Resi.query.all()
    resi_list = []
    for resi in resis:
        resi_list.append(resi.no_resi)
    while True:
        random_number = random.randint(120000000,130000000)
        if random_number not in resi_list:
            return random_number

def get_date():
    today = date.today()
    return today.strftime("%d/%m/%Y")

def get_city():
    city = Kota_Ongkir.query.all()
    list_city = []
    list_city.append(('0','Pilih Kota'))
    for kota in city:
        list_city.append((kota.city_id,kota.city_name))
    return list_city

user_resi = db.Table(
'user_resi',
db.Column('user_id',db.Integer(),db.ForeignKey('user.id')),
db.Column('resi_id',db.Integer(),db.ForeignKey('resi.id'))
)

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
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


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

class Kota(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    cabang_name = db.Column(db.String(length=30),nullable=False)
    kabkota_name = db.Column(db.String(length=30),nullable=False)
    address = db.Column(db.String(length=60),nullable=False)
    kodePos = db.Column(db.String(length=30),nullable=False)


class Kota_Ongkir(db.Model):
    id =db.Column(db.Integer(),primary_key=True)
    city_id = db.Column(db.String(length=30),nullable=False)
    city_name = db.Column(db.String(length=30),nullable=False)

    def cekongkir(self,tujuan,berat):
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
        if data['rajaongkir']['results'][0]['costs'] != []:
            data = data['rajaongkir']['results'][0]['costs'][0]['cost'][0]['value']
            return data
        return 10000*(berat/1000)

    



b = User(username='bbb',roles='user',fullname='bbb',email_address='bbb',password='bbb')
e = User(username='eee',roles='user',fullname='eee',email_address='eee',password='eee')
c = Resi(no_resi=120223212,sender_n='sumanto',receiver_n='sutrisno',origin_n='jl.bojongsoang',destination_n='jl.kantor baru',type_of_packet='baju',type_of_service='reguler',sender_pn=628123,receiver_pn=62847221,weight_packet='2.4kg',arrived_at='bali',time_on_update='12.44 selasa 16/11/22',time_on_deliver='16/11/22',ongkir='12000')
d = Resi(no_resi=120223213,sender_n='sutrisno',receiver_n='habibi',origin_n='jl.sedrisna',destination_n='jl.kertajaya',type_of_packet='baju',type_of_service='reguler',sender_pn=628123,receiver_pn=62847221,weight_packet='2.4kg',arrived_at='bali',time_on_update='12.44 selasa 16/11/22',time_on_deliver='16/11/22',ongkir='12000')
