from tastypie import fields
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS, ALL
from tastypie.authentication import Authentication
from tastypie.authorization import DjangoAuthorization
from core.models import *
from core.helpers.strip_tags import strip


class VideoResource(ModelResource):
    #I guess it should be expected that the user first grabs the video, gets the id, and then grabs the notes.
    #neither have to know about the other.
    #notes = fields.ToManyField('core.api.resources.NoteResource', 'note_set')
    
    class Meta:
        queryset = Video.objects.all()
        resource_name = "video"
        ordering = ['-time',]
        list_allowed_methods = ['get',]
        detail_allowed_methods = ['get',]
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
        if bundle.data is not None:
            text = strip(bundle.data['text'])
            offset = bundle.data['offset']
            video = Video.objects.get(id = bundle.data['video'])
            user = request.user
            user_name = request.user.username
            private = bundle.data['private_note']
            source_link = strip(bundle.data['source_link'])
            note = Note(text = text, offset = offset, video = video, user = user,
                        user_name = user_name, private = private, type = 'note', source='tv', source_link = source_link)
            
            note.save()
            
            
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
        
        
        
        