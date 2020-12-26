from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User

from .forms import CustomUserChangeForm, CustomUserCreationForm


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = (
        'email', 'first_name', 'last_name', 'is_staff',
    )
    list_filter = (
        'is_staff', 'is_active',
    )
    fieldsets = (
        (None, {
            'fields': (
                'email', 'fullname', 'first_name', 'last_name', 'phone',
            )
        }),
        ('Permissions', {
            'fields': (
                'is_staff', 'is_active',
            )
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name', 'last_name',  'phone',
                'password1', 'password2', 'is_staff', 'is_active',
            )
        }
         ),
    )
    search_fields = ('email', 'first_name', 'last_name',)
    ordering = ('email',)

    readonly_fields = ('fullname', )

    def fullname(self, obj: User) -> str:
        return f'{obj.first_name} {obj.last_name}'
