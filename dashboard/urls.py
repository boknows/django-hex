from django.conf.urls import url
from django.contrib import admin

from views import home, create_game, start_game_submit

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/', home, name='home'),
    url(r'^create_game/', create_game, name='create_game'),
    url(r'^start_game_submit/$', start_game_submit, name='start_game_submit'),
]
