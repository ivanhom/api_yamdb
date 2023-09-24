from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import MyUser


class MyUserAdmin(UserAdmin):
    list_display = (
        'id', 'username', 'email', 'first_name', 'last_name', 'bio', 'role'
    )
    search_fields = ('username', 'email')
    list_editable = ('role',)
    list_filter = ('role',)
    list_display_links = ('username',)


MyUserAdmin.fieldsets += (
    ('Extra Fields', {'fields': ('bio', 'role')}),
)

admin.site.register(MyUser, MyUserAdmin)
