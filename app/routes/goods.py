# app/routes/goods.py
from flask import Blueprint, render_template, request, redirect, url_for
from app.models import db, Goods, Record
from app import login_required

# 参数"goods"是蓝图名字，url_for会用到这个名字
bp_goods = Blueprint("goods", __name__)


@bp_goods.route("/")
@login_required
def index():
    # D蓝图内部url_for语法：url_for("蓝图名.函数名")
    return redirect(url_for("goods.goods_list"))


@bp_goods.route("/goods/add", methods=["GET", "POST"])
@login_required
def goods_add():
    if request.method == "GET":
        return render_template("goods_add.html")
    else:
        title = request.form.get("title", "")
        stock_str = request.form.get("stock", "0")
        description = request.form.get("description", "")

        if not title.strip():
            return render_template("message.html", is_error=True, msg="物资名称不能为空",
                                   back_url=url_for("goods.goods_add"))
        if not stock_str.isdigit():
            return render_template("message.html", is_error=True, msg="库存必须输入有效数字",
                                   back_url=url_for("goods.goods_add"))
        stock = int(stock_str)
        if stock < 0:
            return render_template("message.html", is_error=True, msg="库存不能填写负数",
                                   back_url=url_for("goods.goods_add"))

        new_goods = Goods(title=title.strip(), stock=stock, description=description.strip())
        try:
            db.session.add(new_goods)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return render_template("message.html", is_error=True, msg=f"数据库保存失败：{str(e)}",
                                   back_url=url_for("goods.goods_add"))

        return render_template("message.html", is_error=False, msg="物资新增成功！",
                               back_url=url_for("goods.goods_list"))


@bp_goods.route("/goods/list")
@login_required
def goods_list():
    # 获取url上面的page参数
    page = request.args.get("page", 1, type=int)
    per_page = 5
    # paginate
    pagination = Goods.query.paginate(page=page, per_page=per_page, error_out=False)
    goods_list = pagination.items
    return render_template("goods_list.html", goods_list=goods_list, pagination=pagination)


@bp_goods.route("/goods/edit/<int:gid>", methods=["GET", "POST"])
@login_required
def goods_edit(gid):
    goods_item = Goods.query.get(gid)
    if not goods_item:
        return render_template("message.html", is_error=True, msg="该物资不存在",
                               back_url=url_for("goods.goods_list"))
    if request.method == "GET":
        return render_template("goods_edit.html", item=goods_item)
    else:
        new_title = request.form.get("title", "").strip()
        stock_input = request.form.get("stock", "")
        new_description = request.form.get("description", "").strip()

        if not new_title:
            return render_template("message.html", is_error=True, msg="物资名称不能为空",
                                   back_url=url_for("goods.goods_list"))
        if not stock_input.isdigit():
            return render_template("message.html", is_error=True, msg="库存必须填写有效数字",
                                   back_url=url_for("goods.goods_list"))
        new_stock = int(stock_input)
        if new_stock < 0:
            return render_template("message.html", is_error=True, msg="库存不能为负数",
                                   back_url=url_for("goods.goods_list"))

        goods_item.title = new_title
        goods_item.stock = new_stock
        goods_item.description = new_description

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return render_template("message.html", is_error=True, msg=f"修改失败：{str(e)}",
                                   back_url=url_for("goods.goods_list"))
        return redirect(url_for("goods.goods_list"))


@bp_goods.route("/goods/del/<int:gid>", methods=["POST"])
@login_required
def goods_del(gid):
    goods_item = Goods.query.get(gid)
    if not goods_item:
        return render_template("message.html", is_error=True, msg="物资不存在",
                               back_url=url_for("goods.goods_list"))

    record_count = Record.query.filter_by(goods_id=gid).count()
    if record_count > 0:
        return render_template("message.html", is_error=True,
                               msg=f"该物资存在{record_count}条领用记录，禁止删除！请先清空领用记录",
                               back_url=url_for("goods.goods_list"))
    try:
        db.session.delete(goods_item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return render_template("message.html", is_error=True, msg=f"删除失败：{str(e)}",
                               back_url=url_for("goods.goods_list"))
    return redirect(url_for("goods.goods_list"))
