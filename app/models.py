# app/models.py
from enum import unique

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# 创建db对象，不初始化app，解决循环导入
db = SQLAlchemy()


# 用户表
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False, comment="登陆账号")
    _password = db.Column("password", db.String(200), nullable=False, comment="加密后的密码")
    role = db.Column(db.String(20), default="admin", comment="角色: super_admin-超级管理员 admin-普通管理员")

    # 加盐
    def set_password(self, raw_pwd):
        self._password = generate_password_hash(raw_pwd)

    # 明文
    def check_password(self, raw_pwd):
        return check_password_hash(self._password, raw_pwd)


# 物资表
class Goods(db.Model):
    __tablename__ = 'goods'
    id = db.Column(db.Integer, primary_key=True, comment="主键id")
    title = db.Column(db.String(50), nullable=False, comment="物资名称")
    stock = db.Column(db.Integer, default=0, comment="库存数量")
    description = db.Column(db.String(200), comment="物资描述")


# 领用记录表
class Record(db.Model):
    __tablename__ = 'record'
    id = db.Column(db.Integer, primary_key=True)
    goods_id = db.Column(db.Integer, db.ForeignKey('goods.id'), nullable=False, comment="关联物资ID")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, comment="操作人")
    take_num = db.Column(db.Integer, nullable=False, comment="领用数量")
    create_time = db.Column(db.DateTime, default=db.func.now(), comment="领用时间")
    # 外键关系，方便联表查询
    goods = db.relationship('Goods', backref=db.backref('record_list', lazy=True))
    user = db.relationship('User', backref=db.backref('record_list', lazy=True))
