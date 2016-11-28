from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from views import create_map, game, GameList, GameDetail, UserList, UserDetail, api_root, game_test

urlpatterns = [
    url(r'^create_map/', create_map, name='create_map'),
    url(r'^game/(?P<gid>\d+)', game, name='game'),
    url(r'^$', api_root),
    url(r'^game_test/$', game_test),
    url(r'^games/$', GameList.as_view()),
    url(r'^games/(?P<pk>[0-9]+)/$', GameDetail.as_view()),
    url(r'^users/$', UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
