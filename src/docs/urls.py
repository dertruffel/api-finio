from django.conf import settings
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = []

if settings.DEBUG:
    urlpatterns += [
        path('', SpectacularAPIView.as_view(), name='schema'),
        path('schema/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
        ]

