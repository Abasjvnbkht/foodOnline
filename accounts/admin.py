from django.contrib import admin
from .models import User, UserProfile, Vendor
from django.contrib.auth.admin import UserAdmin


class CostumUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name',
                    'username', 'role', 'is_active')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class VendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'vendor_name', 'is_approved', 'created_at')
    list_display_links = ('user', 'vendor_name')


admin.site.register(Vendor, VendorAdmin)


admin.site.register(User, CostumUserAdmin)
admin.site.register(UserProfile)
