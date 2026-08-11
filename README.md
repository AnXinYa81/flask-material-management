# 物资领用管理系统 | Flask Inventory Management System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-green.svg)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-orange.svg)](https://www.sqlalchemy.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> 基于 Flask + SQLAlchemy + MySQL 的轻量级物资领用管理系统  
> A lightweight inventory management system built with Flask + SQLAlchemy + MySQL

---

## 功能特性 | Features

- 物资管理（新增 / 编辑 / 删除保护）| CRUD for inventory items
- 领用登记（自动扣减库存）| Borrow with auto stock deduction
- 领用流水查询（兼容脏数据展示）| Transaction history with dirty data protection
- 权限分级（超级管理员 / 普通管理员）| Role-based access control
- 后端参数校验（防止负数库存）| Backend validation
- 统一消息提示 + 全局异常捕获 | Unified message page + error handling

---

## 技术栈 | Tech Stack

- Python 3.8+
- Flask 2.x
- Flask-SQLAlchemy
- MySQL
- Jinja2
- python-dotenv

---

## 快速开始 | Quick Start

### 1. 克隆项目 | Clone

git clone https://github.com/AnXinYa81/flask-material-management.git
cd flask-material-management

### 2. 创建虚拟环境并安装依赖 | Setup virtual environment

python -m venv .venv
.venv\Scripts\activate
pip install flask flask-sqlalchemy pymysql python-dotenv

### 3. 配置环境变量 | Configure .env

在项目根目录创建 .env 文件，填写你的 MySQL 配置：

DB_USER=你的MySQL用户名
DB_PASSWORD=你的MySQL密码
DB_HOST=localhost
DB_PORT=3306
DB_NAME=flask_system

### 4. 启动项目 | Run

python run.py

访问地址：http://127.0.0.1:5000

默认管理员账号：admin / 123456

---

## 项目结构 | Project Structure

flask-material-management/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── auth/
│   ├── goods/
│   ├── record/
│   └── templates/
├── .env
├── .gitignore
├── run.py
└── README.md

---

## 权限说明 | Permission System

| 角色 | 权限 |
|------|------|
| 超级管理员 | 全部功能 + 管理其他管理员 |
| 普通管理员 | 物资管理 + 领用登记（不能管理用户） |

---

## License

MIT © AnXinYa81