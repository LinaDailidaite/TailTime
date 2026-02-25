from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static, settings
from django.views.generic import RedirectView

urlpatterns = ([
    path('admin/', admin.site.urls),
    path('', include('pets.urls')),
    path('', RedirectView.as_view(url='pets/', permanent=True)),
    path('accounts/', include('django.contrib.auth.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
