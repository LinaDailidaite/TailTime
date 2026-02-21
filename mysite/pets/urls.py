from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('salons/', views.salons, name='salons'),
    path('salons/<int:salon_id>', views.salon, name='salon'),
    path('services/', views.ServiceListView.as_view(), name='services'),
    path('services/<int:pk>', views.ServiceDetailView.as_view(), name='service'),
    path('search/', views.search, name='search'),
    path("mybookings/", views.MyBookingListView.as_view(), name="mybookings"),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
]