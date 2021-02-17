from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Member

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Member
    list_display = ('memberId', 'email', 'name', 'is_staff', 'is_active',)
    list_filter = ('memberId', 'email', 'name', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('memberId', 'email', 'name', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('memberId', 'email', 'name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('memberId',)
    ordering = ('memberId',)

admin.site.register(Member, CustomUserAdmin)