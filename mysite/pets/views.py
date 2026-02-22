from django.http import HttpResponse
from .models import Booking, Salon, Service
from django.views import generic
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.shortcuts import render, reverse
from .forms import ServiceReviewForm
from django.views.generic.edit import FormMixin
from django.contrib.auth.models import User
from .forms import CustomUserChangeForm
from .forms import CustomUserCreateForm
from .forms import BookingCreateUpdateForm
from django.utils import timezone

def salons(request):
    salons = Salon.objects.all()
    context = {
        'salons': salons
    }
    print(salons)
    return render(request, template_name='salons.html', context=context)


def salon(request, salon_id):
    salon = Salon.objects.get(pk=salon_id)
    return render(request, template_name='salon.html', context={'salon': salon})

class ServiceListView(generic.ListView):
    model = Service
    template_name = "services.html"
    context_object_name = "services"
    paginate_by = 6


class ServiceDetailView(FormMixin, generic.DetailView):
    model = Service
    template_name = "service.html"
    context_object_name = "service"
    form_class = ServiceReviewForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.get_form()
        return context

    def get_success_url(self):
        return reverse("service", kwargs={"pk": self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.service = self.get_object()
        form.instance.reviewer = self.request.user
        form.save()
        return super().form_valid(form)


def index(request):
    num_salons = Salon.objects.all().count()
    num_services = Service.objects.all().count()
    num_bookings_in_progress = Booking.objects.filter(status__exact='p').count()
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1


    context = {
        'num_salons': num_salons,
        'num_services': num_services,
        'num_bookings_in_progress': num_bookings_in_progress,
        'num_visits': num_visits,
    }

    return render(request, template_name='index.html', context=context)

def search(request):
    query = request.GET.get('query')

    service_search_results = Service.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query) | Q(salon__name__icontains=query))

    salon_search_results = Salon.objects.filter(
        Q(name__icontains=query) | Q(city__icontains=query) | Q(address__icontains=query) | Q(description__icontains=query))

    context = {
        "query": query,
        "services": service_search_results,
        "salons": salon_search_results,
    }
    return render(request, template_name="search.html", context=context)


class MyBookingListView(LoginRequiredMixin, generic.ListView):
    model = Booking
    template_name = "my_bookings.html"
    context_object_name = "bookings"

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('date_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()

        context['upcoming_bookings'] = self.get_queryset().filter(date_time__gte=now)
        context['past_bookings'] = self.get_queryset().filter(date_time__lt=now)

        return context

class SignUpView(generic.CreateView):
    form_class = CustomUserCreateForm
    template_name = "signup.html"
    success_url = reverse_lazy("login")

class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = CustomUserChangeForm
    template_name = "profile.html"
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user



# LIST VIEW
class BookingListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = Booking
    context_object_name = "bookings"
    template_name = "bookings.html"

    def test_func(self):
        return self.request.user.is_staff

# DETAIL VIEW
class BookingDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Booking
    context_object_name = "booking"
    template_name = "booking_detail.html"

    def test_func(self):
        return self.request.user.is_staff

# CREATE VIEW
class BookingCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Booking
    template_name = "booking_form.html"
    form_class = BookingCreateUpdateForm
    success_url = reverse_lazy('bookings')

    def test_func(self):
        return self.request.user.is_staff

# UPDATE VIEW
class BookingUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Booking
    template_name = "booking_form.html"
    form_class = BookingCreateUpdateForm

    def get_success_url(self):
        return reverse("booking-detail", kwargs={"pk": self.object.pk})

    def test_func(self):
        return self.request.user.is_staff

# DELETE VIEW
class BookingDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Booking
    template_name = "booking_delete.html"
    context_object_name = "booking"
    success_url = reverse_lazy('bookings')

    def test_func(self):
        return self.request.user.is_staff