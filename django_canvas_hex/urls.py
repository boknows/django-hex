from django.conf.urls import url, include
from django.contrib import admin

from map import urls as map_urls
from authentication import urls as auth_urls
from dashboard import urls as dashboard_urls
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^map/', include(map_urls, namespace='map')),
    url(r'^authentication/', include(auth_urls, namespace='authentication')),
    url(r'^dashboard/', include(dashboard_urls, namespace='dashboard')),
]
