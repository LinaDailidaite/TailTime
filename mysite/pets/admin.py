from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Salon, Service, Booking

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {'fields': ('phone_number', 'is_salon_owner', 'photo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {'fields': ('phone_number', 'is_salon_owner', 'photo')}),
    )

class SalonAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'owner', 'display_services']
    list_filter = ['city']
    search_fields = ['name', 'city']

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'salon']
    list_filter = ['name']
    search_fields = ['name']

class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'salon', 'date_time', 'status']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Salon, SalonAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Booking, BookingAdmin)