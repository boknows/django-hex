from django.conf.urls import url

from map.views import create_map

urlpatterns = [
    url(r'^create_map/', create_map, name='create_map'),
]
