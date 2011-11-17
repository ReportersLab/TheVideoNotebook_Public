from tastypie import fields
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS, ALL
from tastypie.authentication import Authentication
from tastypie.authorization import DjangoAuthorization
from core.models import *
from core.helpers.strip_tags import strip
from datetime import datetime, timedelta


class VideoResource(ModelResource):
    #I guess it should be expected that the user first grabs the video, gets the id, and then grabs the notes.
    #neither have to know about the other.
    #notes = fields.ToManyField('core.api.resources.NoteResource', 'note_set')
    
    def obj_create(self, bundle, request = None, **kwargs):
        video = None
        if bundle.data is not None:
            title = strip(bundle.data['title'])
            description = strip(bundle.data['description'])
            time = bundle.data['time']
            user = request.user
            user_name = request.user.username
            private = bundle.data['private']
            video_url = strip(bundle.data['video_url'])
            type = strip(bundle.data['type'])
            
            #Video File would probably be uploaded separately? I don't really know how to handle that yet.
            #video_file = strip(bundle.data['video_file'])
            if type == 'youtube':
                time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.000Z')
            
            video, created = Video.objects.get_or_create(title = title, description = description, time = time, user = user,
                        user_name = user_name, private = private, type = type, video_url = video_url)
            
            video.save()
            
            
        return video
    
    def obj_update(self, bundle, request = None, **kwargs):
        video = None
        if bundle.data is not None:
            video = Video.objects.get( id = bundle.data['id'] )
            if video is not None and video.user == request.user:
                return super(VideoResource, self).obj_update(bundle, request, **kwargs)
        return video
                
        
    
    class Meta:
        queryset = Video.objects.all()
        resource_name = "video"
        ordering = ['-time',]
        list_allowed_methods = ['get', 'post', 'put', 'patch',]
        detail_allowed_methods = ['get', 'post', 'put', 'patch',]
        authentication = Authentication()
        authorization = DjangoAuthorization()
        
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
        note = None
        if bundle.data is not None:
            text = strip(bundle.data['text'])
            offset = bundle.data['offset']
            video = Video.objects.get(id = bundle.data['video'])
            user = request.user
            user_name = request.user.username
            private = bundle.data['private_note']
            source_link = strip(bundle.data['source_link'])
            note = Note.objects.create(text = text, offset = offset, video = video, user = user,
                        user_name = user_name, private = private, type = 'note', source='tv', source_link = source_link)
            
        return note
        #return super(NoteResource, self).obj_create(bundle, request, **kwargs)
    
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
        authentication = Authentication()
        authorization = DjangoAuthorization()
        
        
        
        