from django.utils import timezone
from .models import ServiceReview
from django import forms
from django.contrib.auth.models import User
from .models import CustomUser, Booking, Service
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

class ServiceReviewForm(forms.ModelForm):
    class Meta:
        model = ServiceReview
        fields = ['content']
        labels = {
            'content': _("Comment"),
        }

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'photo']
        labels = {
            'first_name': _("First name"),
            'last_name': _("Last name"),
            'email': _("Email"),
            'photo': _("Photo"),
        }

class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email'] # password1 ir 2 UserCreationForm sutvarko pats

class BookingCreateUpdateForm(forms.ModelForm):
    date_time = forms.DateTimeField(
        label=_("Date and time"),
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local', 'class': 'form-control'}
        )
    )
    class Meta:
        model = Booking
        fields = ['user', 'pet', 'pet_name', 'salon', 'service', 'date_time', 'status']
        labels = {
            'user': _("User"),
            'pet': _("Pet type"),
            'pet_name': _("Pet name"),
            'salon': _("Salon"),
            'service': _("Service"),
            'status': _("Status"),
        }
        widgets = {
            'date_time': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                    'style': 'color: #1A4D2E !important; background-color: #ffffff !important;'
                }
            ),
            'pet': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'color: #1A4D2E !important; background-color: #ffffff !important;',
                'placeholder': _('Pet (e.g. Dog, cat, rabbit)')
            }),
            'pet_name': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'color: #1A4D2E !important; background-color: #ffffff !important;',
                'placeholder': _('Pet name')
            }),
        }

    def __init__(self, *args, **kwargs):
        salon_id = kwargs.pop('salon_id', None)
        request_user = kwargs.pop('request_user', None)
        super().__init__(*args, **kwargs)

        if salon_id:
            self.fields['service'].queryset = Service.objects.filter(salon=salon_id)
            self.fields['salon'].widget = forms.HiddenInput()
        else:
            self.fields['service'].queryset = Service.objects.none()

        if request_user and not request_user.is_staff:
            self.fields['user'].widget = forms.HiddenInput()
            self.fields['user'].required = False
            self.fields['status'].widget = forms.HiddenInput()

    def clean_date_time(self):
        date_time = self.cleaned_data.get('date_time')
        if date_time and date_time < timezone.now():
            raise forms.ValidationError(_("Can't book time in the past!"))
        return date_time