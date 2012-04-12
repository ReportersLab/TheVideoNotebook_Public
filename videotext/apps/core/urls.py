from django.conf import settings
from django.conf.urls.defaults import *
from core import views
from django.views.decorators.cache import cache_page

from tastypie.api import Api
from api.resources import VideoResource, NoteResource, UserResource, SourceResource

v1_api = Api(api_name='v1')
v1_api.register(VideoResource())
v1_api.register(NoteResource())
v1_api.register(UserResource())
v1_api.register(SourceResource())


urlpatterns = patterns('',    
    (r'^api/', include(v1_api.urls)),
    url(r'^l/?$', views.login_main_view, name="login_main_view"),
    (r'^l/login/?$', 'django.contrib.auth.views.login'),
    url(r'^l/logout/?$', views.logout_view, name="logout_view"),
    url(r'^video/add/?$', views.add_video_view, name='add_video_view'),
    url(r'^video/(?P<slug>[-\w]+)/?$', views.video_view, name='video_view'),
    url(r'^user/(?P<username>[-\w]+)/?$', views.user_view, name='user_view'),
    url(r'^search/?$', views.search_view, name='search_view'),
    url(r'^video/(?P<slug>[-\w]+)/notes.csv$', views.video_csv_view, name='video_csv_view'),
    url(r'^taggit_autosuggest/list/$', views.list_tags, name='taggit_autosuggest-list'),
    url(r'^crossdomain.xml$','flashpolicies.views.simple', {'domains': ['media.reporterslab.org']}),
    url(r'', views.index_view, name='index_view'),
)