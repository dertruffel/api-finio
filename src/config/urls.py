from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from . import routing

api_urlpatterns = [
    path('', include('api.urls')),
    path('accounts/', include('accounts.urls')),



    ]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urlpatterns)),
    path('docs/', include('docs.urls')),
]
admin.site.site_header = "finio Admin"
admin.site.site_title = "finio Admin Portal"
admin.site.index_title = "Admin Portal"


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
