from django.http import HttpResponse
from django.shortcuts import render
from .models import Booking, Salon, Service
from django.views import generic
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin


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

class ServiceDetailView(generic.DetailView):
    model = Service
    template_name = "service.html"
    context_object_name = "service"

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
        return Booking.objects.filter(user=self.request.user)