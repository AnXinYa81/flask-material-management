from app import create_app
from app.models import db, User

app = create_app()
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username="admin").first():
        admin = User(username="admin", role="super_admin")
        admin.set_password("123456")
        db.session.add(admin)
        db.session.commit()
        print("超级管理员创建成功：admin / admin123")
    else:
        print("管理员已存在")
