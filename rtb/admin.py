from django.contrib import admin

from .models import NetworkAnalyticsRaw

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from rtb.models import FrameworkUser


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UsersInline(admin.StackedInline):
    model = FrameworkUser
    can_delete = False
    # verbose_name_plural = 'users'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UsersInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# old admin
# admin.site.register(NetworkAnalyticsRaw)
