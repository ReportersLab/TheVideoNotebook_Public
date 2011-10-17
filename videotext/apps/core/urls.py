from django.conf import settings
from django.conf.urls.defaults import *
from core import views
from django.views.decorators.cache import cache_page

from tastypie.api import Api
from api.resources import VideoResource, NoteResource

v1_api = Api(api_name='v1')
v1_api.register(VideoResource())
v1_api.register(NoteResource())


urlpatterns = patterns('',
    
    (r'^api/', include(v1_api.urls)),              
    url(r'^video/(?P<slug>[-\w]+)/?$', views.video_view, name='video_view'),
    url(r'^taggit_autosuggest/list/$', views.list_tags, name='taggit_autosuggest-list'),
    url(r'', views.index_view, name='index_view'),
)