from flask import render_template, redirect, flash, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from urllib.parse import urlparse


@app.route("/")
@app.route("/index")
@login_required
def index():
    posts = [
        {"author": {"username": "John"}, "body": "Beautiful day in Portland!"},
        {"author": {"username": "Susan"}, "body": "The Avengers movie was so cool!"},
    ]
    return render_template("index.html", title="Home Page", posts=posts)


@app.route("/login", methods=["GET", "POST"])
def login():
    # 如果当前用户已认证，则重定向到首页
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
    # 表单提交后的处理
    if form.validate_on_submit():
        # 从数据库中查找用户名是否存在
        user = User.query.filter_by(username=form.username.data).first()
        # 用户名不存在或密码错误时的处理
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        # 登录用户并设置记住我选项
        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get("next")
        # 验证 next 参数，并确保重定向到相对路径
        if not next_page or urlparse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)

    # 渲染登录页面
    return render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
def logout():
    logout_user()  # 执行登出操作
    return redirect(url_for("index"))  # 登出后重定向到首页


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)
