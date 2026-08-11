# app/config.py
import os
from dotenv import load_dotenv

# 加载.env环境变量
load_dotenv()

# 数据库配置
SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}"
    f"@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DB')}"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
