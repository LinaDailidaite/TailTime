from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Salon, Service, Booking, ServiceReview


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {'fields': ('phone_number', 'is_salon_owner', 'photo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {'fields': ('phone_number', 'is_salon_owner', 'photo')}),
    )


class SalonAdmin(admin.ModelAdmin):
    # display_services turi būti aprašytas Salon modelyje arba čia,
    # bet kol kas paliekame kaip turėjote
    list_display = ['name', 'city', 'owner']
    list_filter = ['city']
    search_fields = ['name', 'city']


class ServiceAdmin(admin.ModelAdmin):
    # PAKEISTA: 'salon' pakeistas į 'display_salons'
    list_display = ['name', 'price', 'display_salons']
    list_filter = ['name']
    search_fields = ['name']
    # PRIDĖTA: patogus pasirinkimas adminui
    filter_horizontal = ('salon',)

    # PRIDĖTA: funkcija, kuri parodo salonų sąrašą lentelėje
    def display_salons(self, obj):
        return ", ".join([s.name for s in obj.salon.all()])

    display_salons.short_description = 'Salons'


class BookingAdmin(admin.ModelAdmin):
    list_display = ['salon', 'date_time', 'status', 'user']
    list_filter = ['status', 'date_time']
    list_editable = ['status', 'date_time', 'user']
    search_fields = ['user__username', 'service__name']  # Pataisyta, kad ieškotų pagal tekstą
    fieldsets = [
        ('General', {'fields': ('service', 'salon')}),
        ('Availability', {'fields': ('status', 'date_time', 'user')}),
    ]


class ServiceReviewAdmin(admin.ModelAdmin):
    list_display = ['service', 'date_created', 'reviewer', 'content']


# Registracija (įsitikinkite, kad kiekvienas modelis registruojamas tik kartą)
admin.site.register(ServiceReview, ServiceReviewAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Salon, SalonAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Booking, BookingAdmin)