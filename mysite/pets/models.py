from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from tinymce.models import HTMLField
from PIL import Image
import os
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    # Pridėtas _() prie verbose_name ir kitų laukų
    phone_number = models.CharField(_("Phone number"), max_length=15, blank=True, null=True)
    is_salon_owner = models.BooleanField(_("Is salon owner"), default=False)
    photo = models.ImageField(_("Photo"), upload_to="profile_pics", null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo and os.path.exists(self.photo.path):
            img = Image.open(self.photo.path)
            min_side = min(img.width, img.height)
            left = (img.width - min_side) // 2
            top = (img.height - min_side) // 2
            right = left + min_side
            bottom = top + min_side
            img = img.crop((left, top, right, bottom))
            img = img.resize((300, 300), Image.LANCZOS)
            img.save(self.photo.path)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

class Salon(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=200)
    city = models.CharField(verbose_name=_("City"), max_length=50)
    address = models.CharField(verbose_name=_("Address"), max_length=100)
    description = HTMLField(verbose_name=_("Description"), max_length=3000, default="")
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name=_("Owner"))
    image = models.ImageField(_('Image'), upload_to='Images', null=True, blank=True)

    class Meta:
        verbose_name = _('Salon')
        verbose_name_plural = _('Salons')

    def __str__(self):
        return f"{self.name}, {self.city}"

    def display_services(self):
        return ', '.join(service.name for service in self.services.all())

    display_services.short_description = _('Services')

class Service(models.Model):
    salon = models.ManyToManyField(Salon, verbose_name=_("Salon"), blank=True, related_name="services")
    name = models.CharField(verbose_name=_("Name"), max_length=200)
    description = models.TextField(verbose_name=_("Description"), max_length=500)
    price = models.DecimalField(verbose_name=_("Price"), max_digits=10, decimal_places=0)
    duration_time = models.IntegerField(verbose_name=_("Duration Time (min)"))

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')

    def __str__(self):
        return f"{self.name} - {self.price}€"

class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name=_("User"), null=True, blank=True)
    pet = models.CharField(max_length=50, verbose_name=_("Pet (e.g. dog, cat, rabbit)"))
    pet_name = models.CharField(max_length=50, verbose_name=_("Pet name"))
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, verbose_name=_("Salon"))
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name=_("Service"))
    date_time = models.DateTimeField(verbose_name=_("Date"), null=True, blank=True)

    LOAN_STATUS = (
        ('c', _('Confirmed')),
        ('p', _('In Progress')),
        ('d', _('Done')),
        ('x', _('Canceled')),
    )

    status = models.CharField(
        verbose_name=_("Status"),
        max_length=2,
        choices=LOAN_STATUS,
        blank=True,
        default='c',
        help_text=_('Booking status'),
    )

    class Meta:
        verbose_name = _('Booking')
        verbose_name_plural = _('Bookings')

    def __str__(self):
        return f"{self.user} - {self.salon} ({self.date_time} {self.status})"

class ServiceReview(models.Model):
    service = models.ForeignKey(to="Service", verbose_name=_("Service"), on_delete=models.SET_NULL, null=True, blank=True, related_name="reviews")
    reviewer = models.ForeignKey(to=CustomUser, verbose_name=_("Reviewer"), on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(verbose_name=_("Date Created"), auto_now_add=True)
    content = models.TextField(verbose_name=_("Content"), max_length=2000)

    class Meta:
        verbose_name = _("Service Review")
        verbose_name_plural = _('Service Reviews')
        ordering = ['-date_created']