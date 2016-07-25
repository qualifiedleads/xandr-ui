from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, UserChangeForm
from django.contrib.auth.models import User
from rtb.models import FrameworkUser, SiteDomainPerformanceReport, NetworkAnalyticsReport, MembershipUserToAdvertiser
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import  CheckboxSelectMultiple
from django.forms import ModelChoiceField
from django.utils.html import format_html
from django.core.urlresolvers import reverse

# Define an inline user form descriptor
class UsersInline(admin.StackedInline):
    model = FrameworkUser
    fields = ('apnexus_user', 'link')
    # list_display = ('apnexus_user', )
    readonly_fields = ('link',)
    # filter_horizontal = ('advertisers',)
    can_delete = False
    # verbose_name_plural = 'users'
    show_change_link = True

    def link(self, obj):
        url = reverse('admin:rtb_frameworkuser_change', args=(obj.pk,))
        return format_html("<a href='{}'>{}</a>", url, 'Change')

    # link.allow_tags = True
    link.short_description = 'Advertiser permissions'

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        obj.save()


        # def save_formset(self, request, form, formset, change):


class MembershipInline(admin.TabularInline):
    model = MembershipUserToAdvertiser
    #fields = ()


class FrameworkUserModel(admin.ModelAdmin):
    model = FrameworkUser
    fields = ('username',)
    readonly_fields = ('username',)
    inlines = (MembershipInline,)

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
    list_display = list(BaseUserAdmin.list_display) + ['advertiser_permission_url']
    show_change_link = True

    def advertiser_permission_url(self, obj):
        url = reverse('admin:rtb_frameworkuser_change', args=(obj.pk,))
        return format_html("<a href='{}'>{}</a>", url, 'Advertiser permissions')

    advertiser_permission_url.short_description = "Click to change advertiser permissions"

# Re-register UserAdmin
admin.site.unregister(User)
# User.USERNAME_FIELD = 'email' This caused error (not unique)
admin.site.register(User, UserAdmin)
admin.site.register(FrameworkUser, FrameworkUserModel)

admin.site.register(NetworkAnalyticsReport, date_hierarchy='hour')
admin.site.register(SiteDomainPerformanceReport, date_hierarchy='day')
