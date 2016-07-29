from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from rtb.models import FrameworkUser, SiteDomainPerformanceReport, NetworkAnalyticsReport, MembershipUserToAdvertiser
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Define an inline user form descriptor
class UsersInline(admin.StackedInline):
    model = FrameworkUser
    fields = ('apnexus_user', 'link')
    readonly_fields = ('link',)
    # filter_horizontal = ('advertisers',)
    can_delete = False
    verbose_name_plural = 'Appnexus'

    def link(self, obj):
        url = reverse('admin:rtb_frameworkuser_change', args=(obj.pk,))
        return format_html("<a href='{}'>{}</a>", url, 'Change')

    # link.allow_tags = True
    link.short_description = 'Advertiser permissions'


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
    list_display = list(BaseUserAdmin.list_display) + ['advertiser_permission_url']
    # show_change_link = True

    # Check existing FrameworkUser
    # FrameworkUser.objects.get_or_create(pk=obj.pk)
    def check_existing_framework_user(self, id):
        try:
            fu = FrameworkUser.objects.get(pk=id)
        except FrameworkUser.DoesNotExist:
            n = FrameworkUser(pk=id)
            n.save_base(raw=True, force_insert=True)

    def add_view(self, *args, **kwargs):
        self.inlines = []
        return super(UserAdmin, self).add_view(*args, **kwargs)

    def change_view(self, *args, **kwargs):
        self.check_existing_framework_user(args[1])
        self.inlines = [UsersInline]
        return super(UserAdmin, self).change_view(*args, **kwargs)

    # def save_formset(self, request, form, formset, change):
    #     return super(UserAdmin, self).save_formset(request, form, formset, change)

    def save_model(self, request, obj, form, change):
        super(UserAdmin,self).save_model(request, obj, form, change)
        self.check_existing_framework_user(obj.pk)

    def advertiser_permission_url(self, obj):
        url = reverse('admin:rtb_frameworkuser_change', args=(obj.pk,))
        return format_html("<a href='{}'>{}</a>", url, 'Advertiser permissions')

    advertiser_permission_url.short_description = "Click to change advertiser permissions"

# Automatically create token for new users
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# Re-register UserAdmin
admin.site.unregister(User)
# User.USERNAME_FIELD = 'email' This caused error (not unique)
admin.site.register(User, UserAdmin)
admin.site.register(FrameworkUser, FrameworkUserModel)

admin.site.register(NetworkAnalyticsReport, date_hierarchy='hour')
admin.site.register(SiteDomainPerformanceReport, date_hierarchy='day')
