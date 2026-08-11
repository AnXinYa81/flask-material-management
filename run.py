# run.py

from app import create_app
from app.models import db, User

# 调用工厂函数，拿到组装完成的app实例
app = create_app()

with app.app_context():
    db.create_all()
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        new_user = User(username="admin", role="super_admin")  # 加了 role
        new_user.set_password("123456")
        db.session.add(new_user)
        db.session.commit()
        print("超级管理员创建成功：admin / 123456")
    else:
        print("管理员已存在")

if __name__ == '__main__':
    app.run(debug=True)
