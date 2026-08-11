# app/routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models import db, User
from app import admin_required

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
@bp_auth.route("/admin/list")
@admin_required
def admin_list():
    users=User.query.all()
    return render_template("admin_list.html",users=users)

@bp_auth.route("/admin/add",methods=["GET", "POST"])
@admin_required
def admin_add():
    if request.method == "GET":
        return render_template("admin_add.html")
    username=request.form.get("username","").strip()
    password=request.form.get("password","").strip()
    role=request.form.get("role","admin")
    if not username or not password:
        return render_template("message.html", is_error=True, msg="账号密码不能为空",
                               back_url=url_for("auth.admin_add"))
    if User.query.filter_by(username=username).first():
        return render_template("message.html", is_error=True, msg="账号已存在",
                               back_url=url_for("auth.admin_add"))
    new_user = User(username=username,role=role)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return render_template("message.html", is_error=False, msg="管理员添加成功",
                           back_url=url_for("auth.admin_list"))
@bp_auth.route("/admin/del/<int:uid>",methods=["POST"])
@admin_required
def admin_del(uid):
    user=User.query.get(uid)
    if not user:
        return render_template("message.html", is_error=True, msg="该管理员不存在",
                               back_url=url_for("auth.admin_list"))
    if user.id ==session.get("user_id"):
        return render_template("message.html", is_error=True, msg="不能删除当前登录的账号",
                               back_url=url_for("auth.admin_list"))
    if user.role == "super_admin":
        super_admin_count = User.query.filter_by(role="super_admin").count()
        if super_admin_count <= 1:
            return render_template("message.html", is_error=True, msg="至少保留一个超级管理员，禁止删除",
                                   back_url=url_for("auth.admin_list"))
    try:
        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return render_template("message.html", is_error=True, msg=f"删除失败：{str(e)}",
                               back_url=url_for("auth.admin_list"))
    return redirect(url_for("auth.admin_list"))
