from django.contrib import admin
from django.template.defaulttags import url
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', include(('sav.urls', 'sav'), namespace='sav')),
    path('herakles', include(('heraklesinfo.urls', 'heraklesinfo'), namespace='herakles')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
