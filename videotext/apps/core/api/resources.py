from tastypie import fields
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS, ALL
from core.models import *


class VideoResource(ModelResource):
    #I guess it should be expected that the user first grabs the video, gets the id, and then grabs the notes.
    #neither have to know about the other.
    #notes = fields.ToManyField('core.api.resources.NoteResource', 'note_set')
    
    class Meta:
        queryset = Video.objects.all()
        resource_name = "video"
        ordering = ['-time',] 
        
class NoteResource(ModelResource):
    
    #video = fields.ForeignKey(VideoResource, 'video')
    
    def dehydrate(self, bundle):
        #bundle.data['offset'] = bundle.obj.gen_offset
        return bundle
    
    
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
        
        ordering = ['offset', 'time', 'end_time', 'creation_time']
        
        
        
        
        