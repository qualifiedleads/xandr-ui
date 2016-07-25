from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, UserChangeForm
from django.contrib.auth.models import User
from rtb.models import FrameworkUser, SiteDomainPerformanceReport, NetworkAnalyticsReport
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import  CheckboxSelectMultiple
from django.forms import ModelChoiceField
from django import forms

type_widget = type(UserChangeForm().fields.get('groups').widget)


# class FrameworkUserForm(forms.ModelForm):
#     class Meta:
#         model = FrameworkUser
#         # fields = '__all__'
#         fields = ('apnexus_user','advertisers')
#         widgets = {
#             'advertisers': type_widget(),
#         }

# Define an inline admin descriptor
# which acts a bit like a singleton
class UsersInline(admin.StackedInline):
    model = FrameworkUser
    fields = ('apnexus_user', 'advertisers')
    # filter_horizontal = ('advertisers',)
    can_delete = False
    # verbose_name_plural = 'users'
    # def get_fields(self, request, obj=None):
    #     return ('apnexus_user','advertisers')

    def get_formset(self, request, obj=None, **kwargs):
        """Returns a BaseInlineFormSet class for use in admin add/change views."""
        res = super(UsersInline, self).get_formset(request, obj, **kwargs)
        if not obj:
            pass
        return res

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'advertisers':
            # kwargs['widget'] = admin.ChoicesFieldListFilter
            pass
        return super(UsersInline, self).formfield_for_dbfield(db_field, **kwargs)
        # ModelChoiceField(AppnexusUser.objects)

            # def get_form(self, request, obj=None, **kwargs):
    #     res = super(UsersInline, self).get_form(request, obj, **kwargs)
    #     if not obj:
    #         pass
    #     return res

    # admin.widgets.FilteredSelectMultiple(
    #     db_field.verbose_name,
    #     db_field.name in self.filter_vertical
    # )

# new User form
class NewUserForm(UserChangeForm):
    class Meta:
        model = FrameworkUser
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions')

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


    # def get_fieldsets(self, request, obj=None):
    #     if not obj:
    #         return self.add_fieldsets
    #     return super(UserAdmin, self).get_fieldsets(request, obj)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(NetworkAnalyticsReport, date_hierarchy='hour')
admin.site.register(SiteDomainPerformanceReport, date_hierarchy='day')
