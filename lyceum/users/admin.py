from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from users.models import Profile


class ProfileInline(admin.TabularInline):
    model = Profile
    can_delete = False
    extra = 0
    readonly_fields = (
        Profile.birthday.field.name,
        Profile.image.field.name,
        Profile.coffee_count.field.name,
    )


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    readonly_fields = ("last_login", "date_joined")


admin.site.register(User, UserAdmin)


__all__ = []
