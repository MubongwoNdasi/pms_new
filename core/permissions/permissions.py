from django.utils.translation import ugettext_lazy as _

ROLE_LIST = (('ADMIN', _('Admin')), ('PHARMACIST', _('Pharmacist')), ('BILLING', _('Billing')))


class Role:

    def __init__(self):
        self.admin = 'ADMIN'
        self.pharmacist = 'PHARMACIST'
        self.superadmin = 'SUPERADMIN'

    def admin(self):
        return self.admin

    def pharmacist(self):
        return self.pharmacist

    def superadmin(self):
        return self.superadmin


class Permission:

    def __init__(self):
        self.admin = 'ADMIN'
        self.pharmacist = 'PHARMACIST'
        self.superadmin = 'SUPERADMIN'

    def has_superadmin_permission(self, role):
        return role in [self.superadmin, ]

    def has_admin_permission(self, role):
        return role in [self.admin, ]

    def has_pharmacist_permission(self, role):
        return role in [self.pharmacist, self.admin]


permission = Permission()
role = Role()