from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from rtb.models import FrameworkUser, SiteDomainPerformanceReport, NetworkAnalyticsReport
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import  CheckboxSelectMultiple



# Define an inline admin descriptor
# which acts a bit like a singleton
class UsersInline(admin.StackedInline):
    model = FrameworkUser
    fields = ('apnexus_user', 'advertisers')
    # readonly_fields = ('apnexusname',)
    # filter_horizontal = ('advertisers',)
    can_delete = False
    # verbose_name_plural = 'users'

def formfield_for_dbfield(self, db_field, **kwargs):
    if db_field.name == 'advertisers':
      kwargs['widget'] = admin.ChoicesFieldListFilter
    return super(UsersInline,self).formfield_for_dbfield(db_field,**kwargs)

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups')}),
        (_('User permissions'), {'fields': ('user_permissions',),'classes': ('collapse', )}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    inlines = (UsersInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(NetworkAnalyticsReport, date_hierarchy='hour')
admin.site.register(SiteDomainPerformanceReport, date_hierarchy='day')
