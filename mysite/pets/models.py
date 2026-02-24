from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import IntegerField
from django.utils import timezone
from django.contrib import admin
from tinymce.models import HTMLField
from PIL import Image
from django.conf import settings
import os
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_salon_owner = models.BooleanField(default=False)
    photo = models.ImageField(("Photo"), upload_to="profile_pics", null=True, blank=True)

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
        verbose_name = ("User")
        verbose_name_plural = ("Users")

class Salon(models.Model):
    name = models.CharField(verbose_name="Name", max_length=200)
    city = models.CharField(verbose_name="City", max_length=50)
    address = models.CharField(verbose_name="Address", max_length=100)
    description = HTMLField(verbose_name="Description", max_length=3000, default="")
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Owner")
    image = models.ImageField('Image', upload_to='Images', null=True, blank=True)


    class Meta:
        verbose_name = _('Salon')
        verbose_name_plural = _('Salons')

    def __str__(self):
        return f"{self.name}, {self.city}"

    def display_services(self):
        return ', '.join(service.name for service in self.services.all())

    display_services.short_description = 'services'

class Service(models.Model):
    # Laukas turi būti čia, ne vidinėje klasėje
    salon = models.ManyToManyField(Salon, verbose_name="Salon", blank=True, related_name="services")
    name = models.CharField(verbose_name="Name", max_length=200)
    description = models.TextField(verbose_name="Description", max_length=500)
    price = models.DecimalField(verbose_name="Price", max_digits=10, decimal_places=0)
    duration_time = models.IntegerField(verbose_name="Duration Time (min)")

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')

    def __str__(self):
        return f"{self.name} - {self.price}€"

class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="User", null=True, blank=True)
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, verbose_name="Salon")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Service")
    date_time = models.DateTimeField(verbose_name=_("Date"), null=True, blank=True)
    def previous_booking(self):
        return self.date_time and timezone.now().date() > self.date_time

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

    def __str__(self):
        return f"{self.user} - {self.salon} ({self.date_time} {self.status})"


class ServiceReview(models.Model):
    service = models.ForeignKey(to="service", verbose_name="service", on_delete=models.SET_NULL, null=True, blank=True, related_name="reviews")
    reviewer = models.ForeignKey(to=CustomUser, verbose_name="Reviewer", on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)
    content = models.TextField(verbose_name="Content", max_length=2000)

    class Meta:
        verbose_name = "Service Review"
        verbose_name_plural = 'Service Reviews'
        ordering = ['-date_created']