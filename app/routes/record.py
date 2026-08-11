# app/routes/record.py
from flask import Blueprint, render_template, request, redirect, url_for
# 跨包导入模型与db对象
from app.models import db, Goods, Record
from app import login_required

# 创建领用模块蓝图对象
bp_record = Blueprint("record", __name__)


@bp_record.route("/record/add", methods=["GET", "POST"])
@login_required
def record_add():
    if request.method == "GET":
        all_goods = Goods.query.all()
        return render_template('record_add.html', goods_list=all_goods)
    else:
        goods_id = request.form.get("goods_id", "")
        take_num_str = request.form.get("take_num", "")

        if not goods_id or not take_num_str.isdigit():
            return render_template("message.html", is_error=True, msg="参数非法",
                                   back_url=url_for("record.record_add"))

        take_num = int(take_num_str)
        if take_num < 0:
            return render_template("message.html", is_error=True, msg="领用数量必须大于0",
                                   back_url=url_for("record.record_add"))

        goods_item = Goods.query.get(goods_id)
        if not goods_item:
            return render_template("message.html", is_error=True, msg="物资不存在",
                                   back_url=url_for("record.record_add"))
        if take_num > goods_item.stock:
            return render_template("message.html", is_error=True,
                                   msg=f"库存不足！当前库存：{goods_item.stock}，申请领用：{take_num}",
                                   back_url=url_for("record.record_add"))

        try:
            new_record = Record(goods_id=goods_item.id, take_num=take_num)
            db.session.add(new_record)
            goods_item.stock = goods_item.stock - take_num
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return render_template("message.html", is_error=True, msg=f"领用失败：{str(e)}",
                                   back_url=url_for("record.record_add"))

        return render_template("message.html", is_error=False, msg="✅领用登记完成，库存已扣减",
                               back_url=url_for("goods.goods_list"))


@bp_record.route("/record/list")
@login_required
def record_list():
    page = request.args.get("page", 1, type=int)
    per_page = 5
    pagination = Record.query.order_by(Record.create_time.desc()).paginate(page=page, per_page=per_page,
                                                                           error_out=False)
    record_list = pagination.items
    return render_template("record_list.html", record_list=record_list, pagination=pagination)
