from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, FeesHistory, LibraryHistory, Student, LibraryReview

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'full_name', 'role', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'full_name')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}), 
        ('Personal info', {'fields': ('full_name', 'phone_number', 'address', 'district', 'state', 'pin_code')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'role')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'full_name', 'phone_number', 'role')
        }),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(FeesHistory)
admin.site.register(LibraryHistory)
admin.site.register(Student)
admin.site.register(LibraryReview)
