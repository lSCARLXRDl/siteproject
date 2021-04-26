from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, FileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    age = StringField('Возраст', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    picture = FileField()
    submit = SubmitField('Зарегистрироваться')
