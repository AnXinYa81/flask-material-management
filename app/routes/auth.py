# app/routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models import db, User

bp_auth = Blueprint("auth", __name__)


# 登录页面 GET展示表单，POST处理登录
@bp_auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        if not username or not password:
            return render_template("message.html", is_error=True, msg="账号密码不能为空",
                                   back_url=url_for("auth.login"))

        user = User.query.filter_by(username=username).first()
        # 判断用户是否存在、密码校验
        if not user or not user.check_password(password):
            return render_template("message.html", is_error=True, msg="账号或者密码错误",
                                   back_url=url_for("auth.login"))

        # 登录成功，把用户id存入session
        session["user_id"] = user.id
        return redirect(url_for("goods.goods_list"))


# 退出登录
@bp_auth.route("/logout")
def logout():
    session.pop("user_id", None)  # 删除session中的用户标识
    return render_template("message.html", is_error=False, msg="已退出登录",
                           back_url=url_for("auth.login"))
