from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('predictor.urls')),  # Include the predictor app's URLs
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),  # Serve favicon.ico
]
