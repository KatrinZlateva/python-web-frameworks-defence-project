from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from news_website_project.accounts.models import Profile
from news_website_project.articles.models import UserModel


class NewsUserAdmin(UserAdmin):
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    model = UserModel
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
            'email', 'username', 'password1', 'password2', 'is_staff', 'is_active', 'groups', 'user_permissions')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(UserModel, NewsUserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
