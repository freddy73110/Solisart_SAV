from django.contrib import admin
from django.template.defaulttags import url
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers
from sav import serializerViews

router = routers.DefaultRouter()
router.register(r'users', serializerViews.UserViewSet)
router.register(r'groups', serializerViews.GroupViewSet)
router.register(r'installations', serializerViews.InstallationViewSet)
router.register(r'fichiers', serializerViews.FichierViewSet)
router.register(r'tickets', serializerViews.TicketViewSet)
router.register(r'NC', serializerViews.NCViewSet)

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', include(('sav.urls', 'sav'), namespace='sav')),
    path('herakles', include(('heraklesinfo.urls', 'heraklesinfo'), namespace='herakles')),
    path('mysolisart2/', include(('mysolisart2.urls', 'heraklesinfo'), namespace='mysolisart2')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include(router.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += router.urls
