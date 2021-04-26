from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import PasswordField, BooleanField, SubmitField, StringField, TextAreaField, FileField, validators
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class ProdForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    content = TextAreaField("Описание")
    price = StringField('Цена')
    picture = FileField()
    submit = SubmitField('Применить')