from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),
    path('', include('museum.urls')),
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
]
