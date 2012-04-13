import datetime
from core.api.resources import NoteResource, VideoResource
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from core.models import *
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.middleware.csrf import get_token
from django.utils import simplejson as json
from django.views.generic.date_based import *

from itertools import chain
from operator import attrgetter
from parsers.tvncsv import export_tvn_csv
from tastypie.authorization import DjangoAuthorization
from tastypie.bundle import Bundle
from tastypie.serializers import Serializer
from uploadify_s3 import uploadify_s3
import json




def index_view(request):
    videos = get_user_visible_objects(Video, request)
    data = {
        'video_list'  : videos,
        'is_index' : True,
    }
    return get_response(template='index.django.html', data=data, request=request)


@login_required
def add_video_view(request):
    #policy, signature = gen_s3_policy()
    options = {}
    timestamp = datetime.datetime.now().strftime('%m-%d-%Y-%H-%M-%S')
    key_pattern = 'tvn/contrib/uploads/%s/%s-${filename}' % (request.user.username, timestamp)
    post_data = {
        'key': key_pattern,
        'success_action_status': "201",
    }
    conditions = {
        'key': {'op': 'starts-with', 'value': 'tvn/contrib/uploads/{0}'.format(request.user.username,)},
        'folder': {'op': 'starts-with', 'value': ''},
        'fileext': {'op': 'starts-with', 'value': ''},
        #'Content-Type': {'op': 'starts-with', 'value': ''},
    }
    up = uploadify_s3.UploadifyS3(
                            uploadify_options=options,
                            post_data=post_data,
                            conditions=conditions
                            )
    uploadify_options = up.get_options_json()
    
    print up.policy_string
    data = {
        'csrf_token': get_token(request),
        'uploadify_options': uploadify_options,
        's3_policy': up.post_data['policy'],
        's3_signature': up.post_data['signature'],
        's3_data': json.dumps(up.options['scriptData']),
        's3_access_key': settings.AWS_ACCESS_KEY_ID,
        'timestamp': timestamp,
    }
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






def search_view(request):
    #get the query text
    q = request.GET.get('q', '')
    date = request.GET.get('date', None)
    type = request.GET.get('type', None)
    
    
    if q == '':
        q = request.POST.get('q', '')
        request.GET.q = q
    terms = q.split()
    
    #loop over the terms and build up a generic query of Q objects
    query = Q()
    if terms:
        for term in terms:
            query &= Q(text__icontains=term)
        
    
    #If there's a date, lets add that range as well.
    if date and (date != 'all'):
        now = datetime.date.today()
        difference = datetime.timedelta(weeks=-1)
        if date == "fortnight":
            difference = datetime.timedelta(weeks=-2)
        if date == "month":
            difference = datetime.timedelta(days=-31)
        if date == "season":
            difference = datetime.timedelta(weeks=-13)
        if date == "year":
            difference = datetime.timedelta(days=-365)
        
        now_diff = now + difference
        query &= Q(time__range = (now_diff, now))
        
    #and if they want a specific note type, add that.
    if type and (type != 'all'):
        query &= Q(type = type)
        
    model_list = list()
    
    #lets see if a specific model is requested.
    
    #get the user visibile notes
    notes = get_user_visible_objects(Note, request)
    #and filter them for only the results we want.
    results = notes.filter(query).order_by('time')

    data = {
        'results':results,
        'results_count': results.count(),
        'q': q,
        'is_search': True,
    }
    
    #And return the results
    return get_response('search.django.html', data=data, request=request)
   



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




import base64
import hmac, sha


def gen_s3_policy():
    expiration_date = datetime.datetime.now() + datetime.timedelta(1,0) #one day in the future.
    policy_string = '''{"expiration": "%s",
        "conditions": [ 
          {"bucket": "media.reporterslab.org"}, 
          ["starts-with", "$key", "/tvn/contrib/uploads/"],
          {"acl": "public-read"},
          ["starts-with","$filename",""],
        ]
    }''' % (expiration_date.strftime('%Y-%m-%dT%H-%M-%S:00Z'))
    
    policy = base64.b64encode(policy_string)
    signature = base64.b64encode(hmac.new(settings.AWS_SECRET_ACCESS_KEY, policy, sha).digest())
    return policy, signature
    
    
    
    
    
    
    
    
    
    
