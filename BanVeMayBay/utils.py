import hashlib

from flask_login import current_user

from BanVeMayBay.models import *
from BanVeMayBay import db


def check_login(username, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    user = User.query.filter(User.username == username,
                             User.password == password)
    user = user.join(roles_users, roles_users.c.user_id == User.id)
    user = user.join(Role, roles_users.c.role_id == Role.id). \
        filter(Role.name == 'user').first()

    return user


def check_login_customer(username, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    user = User.query.filter(User.username == username,
                             User.password == password)
    user = user.join(roles_users, roles_users.c.user_id == User.id)
    user = user.join(Role, roles_users.c.role_id == Role.id). \
        filter(Role.name == 'customer').first()

    return user


def get_user_by_id(user_id):
    return User.query.get(user_id)


def add_user(first_name, last_name, email, username, password, sdt, avatar_path):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(first_name=first_name, last_name=last_name, email=email, username=username, password=password, sdt=sdt, avatar=avatar_path)
    r = Role.query.get(8)
    u.roles.append(r)
    try:
        db.session.add(u)
        db.session.commit()
        return True
    except Exception as ex:
        print(ex)
        return False


def cart_stats(cart):
    total_amount, total_quantity = 0, 0
    if cart:
        for p in cart.values():
            total_quantity = total_quantity + p["quantity"]
            total_amount = total_amount + p["quantity"]*p["gia_ve"]

    return total_quantity, total_amount


def add_receipt(cart):
    if cart:
        hoa_don = HoaDon(nhan_vien_id=2,
                         khach_hang_id=int(p["khach_hang_id"]),
                         tong_tien=p["total_amount"])
        for p in list(cart.values()):
            detail = VeChuyenBay(ghe_id=int(p["ghe_id"]),
                                 chuyen_bay_id=int(p["chuyen_bay_id"]),
                                 khach_hang_id=int(p["khach_hang_id"]),
                                 gia_ve=p["gia_ve"])
            db.session.add(detail)



        try:
            db.session.commit()
            return True
        except Exception as ex:
            print(ex)

    return False