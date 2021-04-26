import sys, os
import requests
from requests import get
from werkzeug.utils import secure_filename
from data.users import User
from data.products import Products
from flask_restful import abort
from data.login_form import LoginForm, ProdForm
from data.register import RegisterForm
from data import db_session
from flask import Flask, render_template, redirect, make_response, jsonify, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'azestxrdctfvygbuhnijmokzsadfgvhbjnkmlknjhbfdxtsaydg1234567890kjhgfdsd3456ujnb'
api_key = "40d1649f-0493-4b70-98ba-98533de7710b"
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("db/db.db")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Wrong login or password", form=form)
    return render_template('login.html', title='Authorization', form=form)


@app.route("/")
@app.route("/index")
def index():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    names = {name.id: (name.surname, name.name) for name in users}
    prods = db_sess.query(Products).all()
    pr = [(f"static/img/{prod.picture}", prod.title, f"{prod.content[0:75]}...", prod.id, prod.price) for prod in prods]
    return render_template("index.html", names=names, prods=pr, title='Главная')


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(Products).filter(Products.id == id).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/add_tov/<int:id>', methods=['GET', 'POST'])
def add_tov(id):
    db_sess = db_session.create_session()
    prod = db_sess.query(Products).filter(Products.id == id).first()
    prod.korz_id = current_user.id
    db_sess.commit()
    return redirect('/')


@app.route('/del_tov/<int:id>', methods=['GET', 'POST'])
def del_tov(id):
    db_sess = db_session.create_session()
    prod = db_sess.query(Products).filter(Products.id == id).first()
    prod.korz_id = -1
    db_sess.commit()
    return redirect('/korz')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/add_product',  methods=['GET', 'POST'])
@login_required
def add_news():
    form = ProdForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        prod = Products()
        prod.title = form.title.data
        prod.content = form.content.data
        prod.picture = form.picture.data
        prod.price = form.price.data
        current_user.news.append(prod)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('add_product.html', title='Добавление товара',
                           form=form)


@app.route('/tovar/<int:id>', methods=['GET', 'POST'])
def tovar(id):
    db_sess = db_session.create_session()
    prods = db_sess.query(Products).filter(Products.id == id).first()
    return render_template('tovar.html', prod=prods, title=prods.title)


@app.route('/try')
def tru():
    return render_template('try.html')


@app.route('/about')
def about():
    return render_template('about.html', title='О нас')


@app.route('/kab')
def kab():
    return render_template('kab.html', title='Личный кабинет')


@app.route('/korz')
def korz():
    db_sess = db_session.create_session()
    prods = db_sess.query(Products).filter(Products.korz_id == current_user.id)
    pr = [(prod.title, prod.price, prod.id) for prod in prods]
    return render_template('korz.html', title='Корзина', prods=pr)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Register', form=form,
                                   message="Passwords don't match")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Register', form=form,
                                   message="This user already exists")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            email=form.email.data,
            address=form.address.data,
            picture=form.picture.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
