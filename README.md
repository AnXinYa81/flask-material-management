# Flask物资领用管理系统
## 项目简介
基于Flask+SQLAlchemy+MySQL开发的简易物资领用管理Web系统。
实现物资新增、编辑、删除保护、领用登记、库存自动扣减、领用流水查询。

## 技术栈
- Python3 Flask
- Flask‑SQLAlchemy ORM
- MySQL
- Jinja2模板
- python‑dotenv环境变量管理

## 项目运行
1. 创建虚拟环境，安装依赖
`pip install flask flask‑sqlalchemy pymysql python‑dotenv`

2. 配置.env文件，填写mysql账号密码端口数据库名

3. 启动项目
`python run.py`

访问地址：http://127.0.0.1:5000/

## 功能清单
1. 物资管理：新增、编辑、删除（有领用记录禁止删除）
2. 领用登记：领用物资自动扣减库存
3. 领用流水查询，兼容脏数据展示
4. 后端参数校验，防止负数库存
5. 统一消息提示页面，全局404/500异常捕获、数据库事务回滚

## 项目架构【Day11工程化拆分】
- app/config.py：配置信息，抽离数据库配置
- app/models.py：数据库ORM模型，所有数据表类
- app/routes：业务路由，Blueprint蓝图分模块
- app/templates：jinja2前端页面
