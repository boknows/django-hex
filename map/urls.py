from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from views import create_map, game, pre_game, GameList, GameDetail, \
    UserList, UserDetail, game_test, TileList, MapDetail, action_detail, \
    update_tiles

urlpatterns = [
    url(r'^create_map/', create_map, name='create_map'),
    url(r'^game/(?P<gid>\d+)', game, name='game'),
    url(r'^pre_game/(?P<gid>\d+)', pre_game, name='pre_game'),
    url(r'^tile_list/(?P<map_id>[0-9]+)/$', TileList.as_view()),
    url(r'^tile_detail/$', update_tiles),
    url(r'^api/(?P<id>[0-9]+)/$', MapDetail.as_view()),
    url(r'^action/$', action_detail),
    url(r'^game_test/$', game_test),
    url(r'^games/$', GameList.as_view()),
    url(r'^games/(?P<id>[0-9]+)/$', GameDetail.as_view()),
    url(r'^users/$', UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
