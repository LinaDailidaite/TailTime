from .models import ServiceReview
from django import forms
from django.contrib.auth.models import User
from .models import CustomUser, Booking
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