from flask import render_template, request, session, jsonify
from sqlalchemy import func, subquery

from BanVeMayBay import app, login, db, utils, decorator
from BanVeMayBay.models import *
import os, json


@app.route('/booking', methods=['get'])
def booking():
    ds_san_bay = SanBay.query.all()

    return render_template('booking.html', ds_san_bay=ds_san_bay)


@app.route('/booking-search', methods=['GET', 'POST'])
def flight_search():
    if request.method == "POST":
        san_bay_di_id = request.form.get('SanBayDi')
        san_bay_den_id = request.form.get("SanBayDen")
        ngay_di = request.form.get("NgayDi")
        san_bay_den = SanBay.query.get(san_bay_den_id)
        san_bay_di = SanBay.query.get(san_bay_di_id)
        ds = db.session.query(ChuyenBay.id, ChuyenBay.thoi_gian_bay, ChuyenBay.ngay_gio)
        ds = ds.filter(ChuyenBay.ngay_gio > ngay_di)
        ds = ds.join(TuyenBay) \
            .filter(TuyenBay.san_bay_di_id == san_bay_di_id) \
            .filter(TuyenBay.san_bay_den_id == san_bay_den_id)
        ds = ds.join(PhieuDatVe) \
            .join(GheMayBay) \
            .add_columns(func.count(GheMayBay.id).label('SoGheDat'))
        ds = ds.join(MayBay) \
            .add_columns((MayBay.tong_so_ghe - func.count(GheMayBay.id)).label('tong')).all()
        ds = enumerate(ds, start=1)
    return render_template('flight_search_list.html', ds=ds, san_bay_den=san_bay_den,
                           san_bay_di=san_bay_di)


@app.route('/booking-seat/', methods=["GET", "POST"])
def seat_booking():
    cb_id = ""
    if request.method == "POST":
        cb_id = request.form.get('chuyen_bay_id')
    ds = db.session.query(ChuyenBay.id)
    ds = ds.filter(ChuyenBay.id == cb_id)
    ds = ds.join(MayBay) \
        .filter(MayBay.id == ChuyenBay.may_bay_id)
    ds = ds.join(GheMayBay) \
        .add_columns(GheMayBay.hang_ghe.label('hang_ghe')) \
        .add_columns(GheMayBay.ten_ghe.label('ten_ghe')) \
        .add_columns(GheMayBay.hang_ve_id.label('hang_ve_id')) \
        .add_columns(GheMayBay.id.label('ghe_id'))
    ds = ds.join(TuyenBay) \
        .join(ChiTietTuyenBay) \
        .filter(GheMayBay.hang_ve_id == ChiTietTuyenBay.hang_ve_id) \
        .add_columns(ChiTietTuyenBay.don_gia.label('gia_ve')).all()

    ds_hang_ghe = db.session.query(GheMayBay.hang_ghe) \
        .join(MayBay) \
        .filter(ChuyenBay.id == cb_id).group_by(GheMayBay.hang_ghe).all()

    return render_template('seat_booking.html', ds=ds, ds_hang_ghe=ds_hang_ghe)


@app.route('/api/cart', methods=['post'])
def add_to_cart():
    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']

    data = json.loads(request.data)

    ghe_id = str(data.get("ghe_id"))
    chuyen_bay_id = str(data.get("chuyen_bay_id"))
    khach_hang_id = str(data.get("khach_hang_id"))
    gia_ve = data.get("gia_ve", 0)

    if ghe_id in cart:
        del cart[ghe_id]
    else:
        cart[ghe_id] = {
            "ghe_id": ghe_id,
            "chuyen_bay_id": chuyen_bay_id,
            "khach_hang_id": khach_hang_id,
            "gia_ve": gia_ve,
            "quantity": 1
        }

    session['cart'] = cart

    quantity, amount = utils.cart_stats(cart)

    return jsonify({
        "total_quantity": quantity,
        "total_amount": amount
    })


@app.route('/payment')
def payment():
    quantity, amount = utils.cart_stats(session.get('cart'))
    cart_info = {
        "total_quantity": quantity,
        "total_amount": amount
    }
    return render_template('payment.html', cart_info=cart_info)


@app.route('/api/pay', methods=['post','get'])
def pay():
    if utils.add_receipt(session.get('cart')):
        del session['cart']

        return jsonify({
            "message": "Add receipt successful!",
            "err_code": 200
        })

    return jsonify({
        "message": "Failed"
    })

if __name__ == '__main__':
    pass
