from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/', views.home, name='home'),
    url(r'^create_game/', views.create_game, name='create_game'),
    url(r'^start_game_submit/$', views.start_game_submit, name='start_game_submit'),
]
