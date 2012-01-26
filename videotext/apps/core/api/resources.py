from tastypie import fields
from tastypie.bundle import Bundle
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS, ALL
from tastypie.authentication import Authentication
from tastypie.authorization import DjangoAuthorization
from core.models import *
from core.helpers.strip_tags import strip
from datetime import datetime, timedelta
from django.db import connection


class VideoResource(ModelResource):
    #I guess it should be expected that the user first grabs the video, gets the id, and then grabs the notes.
    #neither have to know about the other.
    #notes = fields.ToManyField('core.api.resources.NoteResource', 'note_set')
    
    def obj_create(self, bundle, request = None, **kwargs):
        if bundle.data is not None:
            bundle.data['title'] = strip(bundle.data['title'])
            bundle.data['description'] = strip(bundle.data['description'])
            kwargs['user'] = request.user
            kwargs['user_name'] = request.user.username
            bundle.data['video_url'] = strip(bundle.data['video_url'])
            bundle.data['type'] = strip(bundle.data['type'])
            
            #Video File would probably be uploaded separately? I don't really know how to handle that yet.
            #video_file = strip(bundle.data['video_file'])
            if bundle.data['type'] == 'youtube':
                kwargs['time'] = datetime.strptime(bundle.data['time'], '%Y-%m-%dT%H:%M:%S.000Z')
              
            
            try:
                saved_object = self.obj_get(request, video_url = bundle.data['video_url'])
                saved_object = Bundle(obj = saved_object)
            except:
                saved_object = super(VideoResource, self).obj_create(bundle, request, **kwargs)
            return saved_object

            
    
    def obj_update(self, bundle, request = None, **kwargs):
        video = None
        #I somehow got the entire DB wiped, think it was because an id passed here was blank. YIKES.
        if bundle.data['id'] is None:
            return bundle
        
        if bundle.data is not None:
            video = Video.objects.get( id = bundle.data['id'] )
            if video is not None and video.user == request.user:
                return super(VideoResource, self).obj_update(bundle, request, **kwargs)
        return Bundle(obj = video)
                
        
    
    class Meta:
        queryset = Video.objects.all()
        resource_name = "video"
        ordering = ['-time',]
        always_return_data = True
        list_allowed_methods = ['get', 'post', 'put', 'patch',]
        detail_allowed_methods = ['get', 'post', 'put', 'patch',]
        authentication = Authentication()
        authorization = DjangoAuthorization()
        filtering = {
            "slug": ('exact', 'startswith',),
            "title": ALL,
            "video_url": ('exact',),
        }
        
class NoteResource(ModelResource):
    
    #video = fields.ForeignKey(VideoResource, 'video')
    
    def dehydrate(self, bundle):
        #bundle.data['offset'] = bundle.obj.gen_offset
        return bundle
    
    '''
    So it appears that related models don't get saved. (As in, a video id won't be converted to the right video.)
    So ratehr than dealing with the default bundle saving, I'm just creating a new note and saving it myself.
    '''
    def obj_create(self, bundle, request=None, **kwargs):
        if bundle.data is not None:
            bundle.data['text'] = strip(bundle.data['text'])
            kwargs['video'] = Video.objects.get(id = bundle.data['video'])
            kwargs['user'] = request.user
            kwargs['user_name'] = request.user.username
            kwargs['private'] = bundle.data['private_note']
            bundle.data['source_link'] = strip(bundle.data['source_link'])
            kwargs['source'] = 'tv'
        return super(NoteResource, self).obj_create(bundle, request, **kwargs)
    
    #TODO: Searching notes
    #TODO: Filter by limits?
    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(NoteResource, self).build_filters(filters)

        if "q" in filters:
            pass

        return orm_filters
    
    
    class Meta:
        queryset = Note.objects.all()
        resource_name = "note"
        filtering = {
            'video': ALL_WITH_RELATIONS,
            'time': ['gt', 'gte', 'lt', 'lte',]
        }
        ordering = ['offset', 'time', 'end_time', 'creation_time',]
        list_allowed_methods = ['get', 'post', 'put', 'patch',]
        detail_allowed_methods = ['get', 'post', 'put', 'patch',]
        always_return_data = True
        authentication = Authentication()
        authorization = DjangoAuthorization()
        
        
        
        