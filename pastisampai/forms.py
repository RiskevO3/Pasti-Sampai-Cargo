from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,SelectField,PasswordField,IntegerField
from wtforms.validators import Length,DataRequired,ValidationError,Email
from pastisampai.models import User,Resi,get_city





class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')
    
    fullname = StringField(label='full name',validators=[Length(min=2, max=30), DataRequired()])
    username = StringField(label = 'username',validators=[Length(min=2),DataRequired()])
    email = StringField(label = "email",validators=[Email(),DataRequired()])
    password = PasswordField(label = 'Password',validators = [Length(min=2),DataRequired()])
    submit = SubmitField(label="register")

class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Login')

class dropPointForm(FlaskForm):
    searchCity = StringField(label='Masukkan nama kota',validators=[DataRequired()])
    submit = SubmitField()

class checkResiForm(FlaskForm):
    noresi = IntegerField(label='No Resi',validators=[DataRequired()])
    submit = SubmitField()

class updateResiForm(FlaskForm):
    
    def validate_noresi(self,noresi_to_check):
        noresi = Resi.query.filter_by(no_resi=noresi_to_check.data).first()
        if not noresi:
            raise ValidationError('No resi yang anda masukkan salah!')

    noresi = IntegerField(label='No Resi',validators=[DataRequired()])
    tanggal = StringField(label = 'Tanggal',validators=[DataRequired()])
    arrived_at = StringField(label='Lokasi Terkini',validators=[DataRequired()])
    submit= SubmitField()

class addNewOrder(FlaskForm):
    sender_n = StringField(label = 'Nama Pengirim',validators=[DataRequired()])
    receiver_n = StringField(label = 'Nama Pengirim',validators=[DataRequired()])
    origin_n = StringField(label = 'Nama Pengirim',validators=[DataRequired()])
    type_of_packet = StringField(label = 'Nama Pengirim',validators=[DataRequired()])
    type_of_service = SelectField(choices=['Jenis Layanan','Reguler','Ekonomi','Kargo'])
    sender_pn = IntegerField(validators=[DataRequired()])
    receiver_pn = IntegerField(validators=[DataRequired()])
    destination_n = StringField(label = 'Nama Pengirim',validators=[DataRequired()])
    weight_packet = StringField(validators=[DataRequired()])
    kota_asal = SelectField(label='Kota Asal',choices = get_city())
    kota_tujuan = SelectField(label='Kota Asal',choices = get_city())
    submit = SubmitField()

class addUsername(FlaskForm):
    def validate_username_r(self,username_r_to_check):
        username = User.query.filter_by(username=username_r_to_check.data).first()
        if not username:
            raise ValidationError('Username of receiver doesnt exists!')

    def validate_username_d(self,username_d_to_check):
        username = User.query.filter_by(username=username_d_to_check.data).first()
        if not username:
            raise ValidationError('Username of deliver doesnt exists!')

    username_r = StringField(label = 'Nama Penerima',validators=[DataRequired()])
    username_d = StringField(label = 'Nama Pengirim',validators=[DataRequired()])
    submit = SubmitField()
