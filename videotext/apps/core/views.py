import datetime
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from core.models import *
from django.views.generic.date_based import *
from django.utils import simplejson as json
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect
from itertools import chain
from operator import attrgetter
from core.api.resources import NoteResource, VideoResource



def index_view(request):
    data = {
        'video_list'  : Video.objects.all(),
        'is_index' : True,
    }
    return get_response(template='index.django.html', data=data, request=request)


def video_view(request, slug):
    note_resource = NoteResource()
    video_resource = VideoResource()
    
    video = get_object_or_404(Video, slug = slug)
    
    #This could be event_notes, but for now let's load everything.
    #It's about 300K for 2,300 notes. Can't imagine a single video being many more than this...?
    #though eventually we may want to build in some sort of 'load 100 notes and Ajax the rest as needed' system.
    notes = video.all_notes
    
    data = {
        'video' : video,
        'video_json': video_resource.serialize(None, video_resource.full_dehydrate(video), 'application/json'),
        'notes_json': note_resource.serialize(None, [note_resource.full_dehydrate(note) for note in notes], 'application/json')
    }
    return get_response(template='video.django.html', data=data, request=request)


def login_main_view(request):
    return render_to_response('', RequestContext(request))
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')




def get_response(template = 'index.html', data = dict(), request = dict(), mime = 'text/html'):
    auth_form = AuthenticationForm(request.POST)
    auth_message = None
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    if username is not None and password is not None:
        user = authenticate(username = username, password = password)
        if user is not None:
            if user.is_active:
                login(request, user)
            else:
                auth_message = 'Disabled Account'
        else:
            auth_message = "Invalid username or password"
            
    
    generic_data = {
        'auth_form': auth_form,
        'auth_message': auth_message,
    }
    
    data.update(generic_data) # I think this is right.
    return render_to_response(template, data, context_instance = RequestContext(request), mimetype = mime)
    




'''
Django-Taggit-Autosuggest hardcodes the model used in auto-suggesting to "Tag". Since we have a custom model,
this is broken. This is a copy-paste job of the view from there, substituting the correct model.
'''

MAX_SUGGESTIONS = getattr(settings, 'TAGGIT_AUTOSUGGEST_MAX_SUGGESTIONS', 20)


def list_tags(request):
    """
Returns a list of JSON objects with a `name` and a `value` property that
all start like your query string `q` (not case sensitive).
"""
    query = request.GET.get('q', '')
    limit = request.GET.get('limit', MAX_SUGGESTIONS)
    try:
        request.GET.get('limit', MAX_SUGGESTIONS)
        limit = min(int(limit), MAX_SUGGESTIONS) # max or less
    except ValueError:
        limit = MAX_SUGGESTIONS

    tag_name_qs = CustomTag.objects.filter(name__istartswith=query).\
        values_list('name', flat=True)
    data = [{'name': n, 'value': n} for n in tag_name_qs[:limit]]

    return HttpResponse(json.dumps(data), mimetype='application/json')

