from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,SelectField,PasswordField
from wtforms.validators import Length,DataRequired,ValidationError,Email
from pastisampai.models import User


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