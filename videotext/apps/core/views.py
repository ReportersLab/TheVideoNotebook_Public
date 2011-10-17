import datetime
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from core.models import *
from django.views.generic.date_based import *
from django.utils import simplejson as json
from django.conf import settings
from django.db.models import Q
from itertools import chain
from operator import attrgetter



def index_view(request):
    data = {
        'video_list'  : Video.objects.all(),
        'is_index' : True,
    }
    return get_response(template='index.django.html', data=data, request=request)


def video_view(request, slug):
    data = {
        'video' : get_object_or_404(Video, slug = slug),
    }
    return get_response(template='video.django.html', data=data, request=request)




def get_response(template = 'index.html', data = dict(), request = dict(), mime = 'text/html'):
    generic_data = {
        
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

