from django.urls import path, include
from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from admin_tools.urls import urlpatterns as admin_tools_urls

urlpatterns = [
    path('admin_tools/', include(admin_tools_urls)),
    path('', include('main.urls')),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


