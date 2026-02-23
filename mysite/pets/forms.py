from .models import ServiceReview
from django import forms
from django.contrib.auth.models import User
from .models import CustomUser, Booking, Service
from django.contrib.auth.forms import UserCreationForm

class ServiceReviewForm(forms.ModelForm):
    class Meta:
        model = ServiceReview
        fields = ['content']

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'photo']

class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class BookingCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['user', 'salon', 'service', 'date_time', 'status']
        widgets = {'date_time': forms.DateInput(attrs={'type': 'datetime-local'})}

    def __init__(self, *args, **kwargs):
        salon_id = kwargs.pop('salon_id', None)
        super().__init__(*args, **kwargs)

        if salon_id:
            self.fields['service'].queryset = Service.objects.filter(salon_id=salon_id)
            self.fields['salon'].widget = forms.HiddenInput()

        else:
            self.fields['service'].queryset = Service.objects.none()
