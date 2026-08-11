# run.py

from app import create_app
from app.models import db,User

# 调用工厂函数，拿到组装完成的app实例
app = create_app()

with app.app_context():
    db.create_all()
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        new_user = User(username="admin")
        new_user.set_password("123456")
        db.session.add(new_user)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
