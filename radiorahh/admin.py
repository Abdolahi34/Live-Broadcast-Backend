from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib import admin

admin.site.unregister(get_user_model())


# Customizing the admin page in the management panel
@admin.register(get_user_model())
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'last_login', 'date_joined', 'is_staff')
