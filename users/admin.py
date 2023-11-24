from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from users.models import AdminProfile

User = get_user_model()


class AdminProfileInlined(admin.StackedInline):
    model = AdminProfile
    can_delete = False


class UserAdmin(UserAdmin):
    inlines = (AdminProfileInlined,)
    list_display = ('username', 'email', 'is_staff',)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    @admin.display(description='Полное имя')
    def full_name(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name} {obj.patronymic}'

    list_display = ('id', 'full_name', 'birthday')
    list_display_links = ('id', 'full_name', 'birthday')
