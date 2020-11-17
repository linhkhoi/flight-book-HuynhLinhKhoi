from flask_security import RoleMixin, SQLAlchemyUserDatastore, Security, UserMixin

from BanVeMayBay import db, app
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, Time, DateTime, Table
from sqlalchemy.orm import relationship

#e10adc3949ba59abbe56e057f20f883e
# Define models
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __unicode__(self):
        return u"{name} ({role})".format(name=self.name, role=self.description or 'Role')

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    khach_hang = relationship("KhachHang", backref="user", lazy=True)
    nhan_vien = relationship("NhanVien", backref="user", lazy=True)

    def has_roles(self, *args):
        return set(args).issubset({role.name for role in self.roles})

    def __unicode__(self):
        return u"{first_name} ({last_name})".format(first_name=self.first_name, last_name=self.last_name)

    def __str__(self):
        return self.username



# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


class SanBay(db.Model):
    __tablename__ = "san_bay"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten_san_bay = Column(String(50), nullable=False)

    def __str__(self):
        return self.ten_san_bay


class ChiTietTuyenBay(db.Model):
    __tablename__ = 'chi_tiet_tuyen_bay'
    tuyen_bay_id = Column(Integer, ForeignKey('tuyen_bay.id'), primary_key=True)
    hang_ve_id = Column(Integer, ForeignKey('hang_ve.id'), primary_key=True)
    don_gia = Column(Float)
    hangve = relationship("HangVe", back_populates="tuyen_bay")
    tuyenbay = relationship("TuyenBay", back_populates="hang_ve")


class TuyenBay(db.Model):
    __tablename__ = "tuyen_bay"
    id = Column(Integer, primary_key=True, autoincrement=True)
    san_bay_den_id = Column(Integer, ForeignKey(SanBay.id), nullable=False)
    san_bay_di_id = Column(Integer, ForeignKey(SanBay.id), nullable=False)
    san_bay_den_fk = relationship("SanBay", foreign_keys=[san_bay_den_id])
    san_bay_di_fk = relationship("SanBay", foreign_keys=[san_bay_di_id])
    chuyen_bay = relationship("ChuyenBay", backref="tuyenbay", lazy=True)
    hang_ve = relationship("ChiTietTuyenBay", back_populates="tuyenbay")

    def __str__(self):
        return str(self.id)


class HangVe(db.Model):
    __tablename__ = "hang_ve"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten_hang_ve = Column(String(50), nullable=False)
    ve_chuyen_bay = relationship("VeChuyenBay", backref="hangve", lazy=True)
    phieu_dat_ve = relationship("PhieuDatVe", backref="hangve", lazy=True)
    tinh_trang_ve = relationship("TinhTrangVe", backref="hangve", lazy=True)
    tuyen_bay = relationship("ChiTietTuyenBay", back_populates="hangve")

    def __str__(self):
        return str(self.id)






# class MayBay(db.Model):
#     __tablename__ = "may_bay"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     loai_may_bay = Column(String(50), nullable=False)
#     chuyen_bay = relationship("ChuyenBay", backref="maybay", lazy=True)
#
#     def __str__(self):
#         return self.loai_may_bay


class ChuyenBay(db.Model):
    __tablename__ = "chuyen_bay"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngay_gio = Column(DateTime, nullable=False)
    thoi_gian_bay = Column(Time, nullable=False)
    so_ghe_hang_mot = Column(Integer, nullable=False)
    so_ghe_hang_hai = Column(Integer, nullable=False)
    tuyen_bay_id = Column(Integer, ForeignKey(TuyenBay.id), nullable=False)
    chi_tiet_chuyen_bay = relationship("ChiTietChuyenBay", backref="chuyenbay", lazy=True)
    ve_chuyen_bay = relationship("VeChuyenBay", backref="chuyenbay", lazy=True)
    phieu_dat_ve = relationship("PhieuDatVe", backref="chuyenbay", lazy=True)
    doanh_thu_thang = relationship("DoanhThuThang", backref="chuyenbay", lazy=True)
    tinh_trang_ve = relationship("TinhTrangVe", backref="chuyenbay", lazy=True)

    def __str__(self):
        return self.id


class TinhTrangVe(db.Model):
    __tablename__ = "tinh_trang_ve"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chuyen_bay_id = Column(Integer, ForeignKey(ChuyenBay.id), nullable=False)
    hang_ve_id = Column(Integer, ForeignKey(HangVe.id), nullable=False)
    so_ghe_trong = Column(Integer, nullable=False)
    so_ghe_dat = Column(Integer, nullable=False)

    def __str__(self):
        return str(self.id)


class ChiTietChuyenBay(db.Model):
    __tablename__ = "chi_tiet_chuyen_bay"
    id = Column(Integer, ForeignKey(ChuyenBay.id), primary_key=True)
    san_bay_trung_gian_id = Column(Integer, ForeignKey(SanBay.id), nullable=False)
    thoi_gian_dung = Column(Time, nullable=False)

    def __str__(self):
        return self.san_bay_trung_gian


class KhachHang(db.Model):
    __tablename__ = "khach_hang"
    id = Column(Integer, ForeignKey(User.id), primary_key=True)
    cmnd = Column(Integer)
    ve_chuyen_bay = relationship("VeChuyenBay", backref="khachhang", lazy=True)
    phieu_dat_ve = relationship("PhieuDatVe", backref="khachhang", lazy=True)
    hoa_don = relationship("HoaDon", backref="khachhang", lazy=True)

    def __str__(self):
        return self.ten_kh


class NhanVien(db.Model):
    __tablename__ = "nhan_vien"
    id = Column(Integer, ForeignKey(User.id), primary_key=True)
    chuc_vu = Column(String(50),nullable=False)
    hoa_don = relationship("HoaDon", backref="nhanvien", lazy=True)
    doanh_thu_thang = relationship("DoanhThuThang", backref="nhanvien", lazy=True)

    def __str__(self):
        return self.ten_nv


class VeChuyenBay(db.Model):
    __tablename__ = "ve_chuyen_bay"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chuyen_bay_id = Column(Integer, ForeignKey(ChuyenBay.id), nullable=False)
    hang_ve_id = Column(Integer, ForeignKey(HangVe.id), nullable=False)
    khach_hang_id = Column(Integer, ForeignKey(KhachHang.id), nullable=False)
    gia_ve = Column(Float, nullable=False)

    def __str__(self):
        return str(self.id)


class PhieuDatVe(db.Model):
    __tablename__ = "phieu_dat_ve"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chuyen_bay_id = Column(Integer, ForeignKey(ChuyenBay.id), nullable=False)
    hang_ve_id = Column(Integer, ForeignKey(HangVe.id), nullable=False)
    khach_hang_id = Column(Integer, ForeignKey(KhachHang.id), nullable=False)
    gia_ve = Column(Float, nullable=False)
    ngay_dat = Column(DateTime, nullable=False)

    def __str__(self):
        return str(self.id)


class HoaDon(db.Model):
    __tablename__ = "hoa_don"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngay_lap_hoa_don = Column(DateTime, nullable=False)
    khach_hang_id = Column(Integer, ForeignKey(KhachHang.id), nullable=False)
    nhan_vien_id = Column(Integer, ForeignKey(NhanVien.id), nullable=False)
    tong_tien = Column(Float, nullable=False)

    def __str__(self):
        return str(self.id)


class DoanhThuNam(db.Model):
    __tablename__ = "doanh_thu_nam"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nam = Column(Integer)
    tong_tien = Column(Float, nullable=False)
    doanh_thu_thang = relationship("DoanhThuThang", backref="doanhthunam", lazy=True)

    def __str__(self):
        return str(self.id)


class DoanhThuThang(db.Model):
    __tablename__ = "doanh_thu_thang"
    id = Column(Integer, primary_key=True, autoincrement=True)
    thang = Column(Integer, nullable=False)
    doanh_thu_nam_id = Column(Integer, ForeignKey(DoanhThuNam.id), nullable=False)
    nhan_vien_id = Column(Integer, ForeignKey(NhanVien.id), nullable=False)
    chuyen_bay_id = Column(Integer, ForeignKey(ChuyenBay.id), nullable=False)
    so_ve = Column(Integer, nullable=False)
    ty_le = Column(Float, nullable=False)
    tong_tien = Column(Float, nullable=False)

    def __str__(self):
        return str(self.id)


if __name__ == "__main__":
    db.create_all()
