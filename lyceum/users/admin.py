from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import Profile, User


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
    readonly_fields = (
        User.last_login.field.name,
        User.date_joined.field.name,
    )


admin.site.register(User, UserAdmin)
admin.site.unregister(User)
admin.site.register(User)


__all__ = ()
