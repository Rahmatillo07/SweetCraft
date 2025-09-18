from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Cake, Order, Ingredient


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'phone_number', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('phone_number',)}),
        ('Roles & Permissions',
         {'fields': ('role', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'phone_number', 'role', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )

    search_fields = ('username', 'phone_number')
    ordering = ('username',)

admin.site.register(Cake)
admin.site.register(Order)
admin.site.register(Ingredient)