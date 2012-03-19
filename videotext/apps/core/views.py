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
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from itertools import chain
from operator import attrgetter
from core.api.resources import NoteResource, VideoResource
from tastypie.bundle import Bundle
from parsers.tvncsv import export_tvn_csv


def index_view(request):
    videos = get_user_visible_objects(Video, request)
    data = {
        'video_list'  : videos,
        'is_index' : True,
    }
    return get_response(template='index.django.html', data=data, request=request)


@login_required
def add_video_view(request):
    data = {}
    return get_response(template='add_video.django.html', data=data, request=request)


def video_view(request, slug):
    note_resource = NoteResource()
    video_resource = VideoResource()
    
    video = get_user_visible_object(Video, request, slug = slug)
    notes = get_user_visible_objects(Note, request)
    notes = notes.filter(video = video)
    
    data = {
        'video' : video,
        'video_json': video_resource.serialize(None, video_resource.full_dehydrate(Bundle(obj = video)), 'application/json'),
        'notes_json': note_resource.serialize( None, [note_resource.full_dehydrate(Bundle(obj = note)) for note in notes], 'application/json')
    }
    return get_response(template='video.django.html', data=data, request=request)



def user_view(request, username):
    user_info = get_object_or_404(User, username = username)
    videos = get_user_visible_objects(Video, request)
    data = {
        'user_info'   : user_info, 
        'video_list'  : videos.filter(user__username = username),
        'is_index'    : True,
    }
    
    return get_response(template='user.django.html', data=data, request=request)


def video_csv_view(request, slug):
    video = get_object_or_404(Video, slug = slug)
    return export_tvn_csv(video)



def login_main_view(request):
    return render_to_response('', RequestContext(request))
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')








def get_user_visible_objects(model, request):
    #first, figure out if the user should see unpublished objects
    qs = model.published_objects
    if request.user.is_authenticated() and request.user.is_staff:
        qs = model.objects
    
    #now exclude the items where the private is marked AND aren't from this user
    #qs = qs.exclude( Q(private = True) & ~Q(user__id = request.user.id) )
    if request.user.is_authenticated():
        if model is Note:
            qs = qs.exclude( Q(private = True) & ~(Q(user__id = request.user.id) | Q(video__user__id = request.user.id) | Q(import_source__user__id = request.user.id)) )
        else:
            qs = qs.exclude( Q(private = True) & ~Q(user__id = request.user.id) )
    else:
        qs = qs.exclude(private = True)
    return qs


def get_user_visible_object(model, request, **kwargs):
    qs = model.published_objects
    if request.user.is_authenticated() and request.user.is_staff:
        qs = model.objects
        
    #exclude private objects that don't belong to this user
    qs = qs.exclude( Q(private = True) & ~Q(user__id = request.user.id) )
    
    return get_object_or_404(qs, **kwargs)







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

