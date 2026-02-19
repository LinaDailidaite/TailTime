from django.http import HttpResponse
from django.shortcuts import render
from .models import Booking, Salon, Service
from django.views import generic


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


    context = {
        'num_salons': num_salons,
        'num_services': num_services,
        'num_bookings_in_progress': num_bookings_in_progress,
    }

    return render(request, template_name='index.html', context=context)