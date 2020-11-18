from BanVeMayBay import admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, helpers as admin_helpers
from flask import redirect, abort, url_for, request
from flask_login import current_user, logout_user
from BanVeMayBay.models import *


# Create customized model view class
class FlightBaseView(ModelView):

    column_display_pk = True
    page_size = 20
    can_view_details = True
    can_export = True

    def is_accessible(self):

        # set accessibility...
        if not current_user.is_active or not current_user.is_authenticated:
            return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


class regularFlightView(FlightBaseView):

    def is_accessible(self):

        # set accessibility...
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        # roles not tied to ascending permissions...
        if not current_user.has_role('export'):
            self.can_export = False

        # roles with ascending permissions...
        if current_user.has_role('adminrole'):
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
            self.can_export = True
            return True
        if current_user.has_role('supervisor'):
            self.can_create = True
            self.can_edit = True
            self.can_delete = False
            return True
        if current_user.has_role('user'):
            self.can_create = False
            self.can_edit = False
            self.can_delete = False
            return True
        if current_user.has_role('create'):
            self.can_create = True
            self.can_edit = False
            self.can_delete = False
            return True
        if current_user.has_role('read'):
            self.can_create = False
            self.can_edit = False
            self.can_delete = False
            return True
        return False


class SuperView(FlightBaseView):

    can_export = True

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('adminrole'):
            self.column_display_pk = True
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
            return True
        return False


@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
    )


class AboutUsView(BaseView):
    @expose("/")
    def index(self):
        return self.render("admin/about-us.html")

    def is_accessible(self):
        return current_user.is_authenticated


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()

        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


class UserView(SuperView):
    can_view_details = True
    column_list = ['id', 'first_name', 'last_name', 'username', 'password', 'roles', 'active']
    column_default_sort = ('id', False)
    column_filters = [
        'first_name',
        'last_name',
        'username',
        'active',
        'roles.name',
    ]
    column_details_list = [
        'first_name', 'last_name', 'username', 'active', 'roles',
        'confirmed_at', 'last_login_at', 'current_login_at', 'last_login_ip', 'current_login_ip', 'login_count',
    ]
    form_columns = [
        'first_name', 'last_name', 'username', 'active', 'roles', 'password',
    ]


class RoleView(SuperView):
    column_list = ['name', 'description']

    form_columns = ['name', 'description']


admin.add_view(RoleView(Role, db.session))
admin.add_view(UserView(User, db.session))
admin.add_view(regularFlightView(SanBay, db.session))
admin.add_view(regularFlightView(TuyenBay, db.session))
admin.add_view(regularFlightView(ChiTietTuyenBay, db.session))
admin.add_view(regularFlightView(ChuyenBay, db.session))
admin.add_view(regularFlightView(HangVe, db.session))
admin.add_view(regularFlightView(TinhTrangVe, db.session))
admin.add_view(regularFlightView(ChiTietChuyenBay, db.session))
admin.add_view(regularFlightView(KhachHang, db.session))
admin.add_view(regularFlightView(NhanVien, db.session))
admin.add_view(regularFlightView(VeChuyenBay, db.session))
admin.add_view(regularFlightView(PhieuDatVe, db.session))
admin.add_view((AboutUsView(name="US")))
admin.add_view(LogoutView(name="Logout"))

if __name__ == "__main__":
    pass