from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from accounts.models import User
from accounts.forms import UserForm


class CustomUserAdmin(UserAdmin):
    list_display = ['name', 'email', 'is_superuser', 'is_staff']
    list_filter = []
    search_fields = ['name', 'email']
    filter_horizontal = []
    fieldsets = (
        (None, {'fields': ('name', 'email', 'username', 'password')}),
        ('Permissão',
         {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_admin')}),
    )
    add_fieldsets = ((None, {'classes': ('wide',), 'fields': (
        'name', 'username', 'email', 'password1', 'password2',
    )}),)
    forms = UserForm

    


class UserClinicAdmin(admin.ModelAdmin):
    list_display = ['user', 'clinic']


admin.site.register(User, CustomUserAdmin)