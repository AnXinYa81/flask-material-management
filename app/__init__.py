# app/__init__.py
from flask import Flask, render_template, url_for, session, redirect
from .models import db
from .config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from functools import wraps
from app.models import User


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("auth.login"))
        return func(*args, **kwargs)

    return wrapper

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("auth.login"))
        user =User.query.get(session["user_id"])
        if not user or user.role!= "super_admin":
            return render_template("message.html", is_error=True,msg="权限不足，仅超级管理员可访问",
                                   back_url=url_for("goods.goods_list"))
        return func(*args, **kwargs)
    return wrapper


def create_app():
    app = Flask(__name__)
    # session加密密钥
    app.secret_key = "todayflasksecretdoctorabc1234"
    # 加载配置
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

    db.init_app(app)

    # 导入蓝图
    from .routes.goods import bp_goods
    from .routes.record import bp_record
    from .routes.auth import bp_auth
    app.register_blueprint(bp_goods)
    app.register_blueprint(bp_record)
    app.register_blueprint(bp_auth)

    # 全局404错误捕获
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("message.html", is_error=True, msg="404:访问的页面不存在",
                               back_url=url_for("goods.goods_list")), 404

    # 全局500错误捕获
    @app.errorhandler(500)
    def server_error(e):
        return render_template("message.html", is_error=True, msg="500:服务器内部出错，请检查操作",
                               back_url=url_for("goods.goods_list")), 500

    return app
