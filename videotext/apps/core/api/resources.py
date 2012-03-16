from core.models import *
from core.helpers.strip_tags import strip

from tastypie import fields
from tastypie import http
from tastypie.authentication import Authentication
from tastypie.authorization import DjangoAuthorization
from tastypie.bundle import Bundle
from tastypie.exceptions import NotFound, ImmediateHttpResponse
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS, ALL

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.db import connection
from django.db.models import Q

from customfields import TzDateTimeField
         


class VideoResource(ModelResource):
    #I guess it should be expected that the user first grabs the video, gets the id, and then grabs the notes.
    #neither have to know about the other.
    #notes = fields.ToManyField('core.api.resources.NoteResource', 'note_set')
    user = fields.ToOneField('core.api.resources.UserResource', 'user', full = True, null = True, blank = True, readonly = True)
    creation_time = fields.DateField(attribute = 'creation_time', readonly = True)
    update_time  = fields.DateField(attribute = 'update_time', readonly = True)
    published = fields.BooleanField('published', default = True, readonly = True)
    #have to use this because updating the video time caused chaos. This field converts to UTC on output and from UTC on input.
    time = TzDateTimeField(attribute = 'time')
    slug = fields.CharField(attribute = 'slug', readonly = True, null = True, blank = True)
    
    def obj_create(self, bundle, request = None, **kwargs):
        if bundle.data is not None:
            self.strip_bundle_data(bundle)
            #Video File would probably be uploaded separately? I don't really know how to handle that yet.
            #video_file = strip(bundle.data['video_file'])
            if bundle.data['type'] == 'youtube':
                kwargs['time'] = datetime.strptime(bundle.data['time'], '%Y-%m-%dT%H:%M:%S.000Z')
              
            
            try:
                saved_object = self.obj_get(request, video_url = bundle.data['video_url'])
                saved_object = Bundle(obj = saved_object)
            except:
                saved_object = super(VideoResource, self).obj_create(bundle, request, **kwargs)
            
            #do this here because the user property is readonly.    
            saved_object.obj.user = request.user
            saved_object.obj.user_name = request.user.username
            saved_object.obj.save()
            return saved_object

            
    
    def obj_update(self, bundle, request = None, **kwargs):
        video = None
        
        if bundle.data is not None:
            video = Video.objects.get( id = bundle.data['id'] )
            if video is not None and video.user == request.user:
                self.strip_bundle_data(bundle)
                if bundle.data['icon'] is not None:
                    del(bundle.data['icon'])
                if bundle.data['video_file'] is not None:
                    del(bundle.data['video_file'])
                
                
                
                
                return_val = super(VideoResource, self).obj_update(bundle, request, **kwargs)
                #if we're doing a sync, re-save all notes on this video.
                sync = bundle.data.get('sync_notes', False)
                if sync is True:
                    for note in video.note_set.all():
                        #saving updates offset.
                        note.save()
                return return_val
            else:
                raise ImmediateHttpResponse(response=http.HttpUnauthorized())
                #raise PermissionDenied("User Doesn't have permission to edit this video.")
                
        return Bundle(obj = video)
                
    #Theoretically removes any JS injections.
    def strip_bundle_data(self, bundle):
        bundle.data['video_url'] = strip(str(bundle.data.get('video_url', '')))
        bundle.data['type'] = strip(str(bundle.data.get('type', '')))
        bundle.data['title'] = strip(str(bundle.data.get('title', '')))
        bundle.data['description'] = strip(str(bundle.data.get('description', '')))
        bundle.data['icon'] = strip(str(bundle.data.get('icon', '')))
        bundle.data['icon_link'] = strip(str(bundle.data.get('icon_link', '')))
        bundle.data['teaser'] = strip(str(bundle.data.get('teaser', '')))
        #bundle.data['video_file'] = strip(str(bundle.data.get('video_file', '')))
        bundle.data['user_link'] = strip(str(bundle.data.get('user_link', '')))
        
        
        
    '''
    The original save_related function is here: https://github.com/toastdriven/django-tastypie/blob/master/tastypie/resources.py#L1893
    
    My problem is that I'm whitelisting some user fields so I can get a picture of that. Unfortunately, the original save_related just blindly
    saves the related models without checking for that. SO, you end up with a mostly blank model instance (things like Password are gone).
    This is sort of a hack to just ignore saving of related models until something better can be done.
    '''
    def save_related(self, bundle):
        pass

    
    '''
    This is called by put_list, here: https://github.com/toastdriven/django-tastypie/blob/master/tastypie/resources.py#L1070
    
    I've run into an issue where all of the videos get deleted from the DB. this happens when Backbone "PUT"s a JSON request to the server
    without specifying an ID for the object. Basically, it's a bug on my part where Backbone thinks I'm updating but it's actually creating. BUT,
    it seems crazy that the entire video collection could be deleted so easily, and I don't want that to happen accidentally by anyone using the API.
    It also seems strange that this can be called even though 'delete' methods are specifically not allowed in the Meta.
    
    For now I'm going to not allow deleting an entire list to hopefully prevent this. Long-term would be to error-check in put_list as well as ensure
    Backbone doesn't put when I mean post (I have a fix for the Backbone part already). Also need to add user ownership verification.
    '''
    def obj_delete_list(self, request=None, **kwargs):
        pass
    
    
    
    class Meta:
        queryset = Video.objects.all()
        resource_name = "video"
        ordering = ['-time',]
        always_return_data = True
        list_allowed_methods = ['get', 'post',]
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
    
    user = fields.ToOneField('core.api.resources.UserResource', 'user', full = True, null = True, blank = True, readonly = True)
    import_source = fields.ToOneField('core.api.resources.SourceResource', 'import_source', full = False, null = True, blank = True, readonly = True)
    video = fields.ToOneField('core.api.resources.VideoResource', 'video', full = False, null = True, blank = True, readonly = True)
    
    creation_time = fields.DateField(attribute = 'creation_time', readonly = True)
    update_time  = fields.DateField(attribute = 'update_time', readonly = True)
    #have to use this because updating the video time caused chaos. This field converts to UTC on output and from UTC on input.
    time = TzDateTimeField(attribute = 'time', null = True, blank = True)
    published = fields.BooleanField('published', default = True, readonly = True)
    type = fields.CharField(attribute = 'type', readonly = False, blank = True, null = True)
    source_link = fields.CharField(attribute = 'source_link', readonly = True, blank = True, null = True)
    source = fields.CharField(attribute = 'source', readonly = True, blank = True, null = True)
    original_source = fields.CharField(attribute = 'original_source', readonly = True, blank = True, null = True)
    original_source_link = fields.CharField(attribute = 'original_source_link', readonly = True, blank = True, null = True)
    original_data = fields.CharField(attribute = 'original_data', readonly = True, blank = True, null = True)
    
    
    '''
    So it appears that related models don't get saved. (As in, a video id won't be converted to the right video.)
    So rather than dealing with the default bundle saving, I'm just creating a new note and saving it myself.
    '''
    def obj_create(self, bundle, request=None, **kwargs):
        if bundle.data is not None:
            self.strip_bundle_data(bundle)
            saved_object = super(NoteResource, self).obj_create(bundle, request, **kwargs)
            #do this here because the user property is readonly.    
            saved_object.obj.user = request.user
            saved_object.obj.user_name = request.user.username
            saved_object.obj.source = 'TheVideoNotebook'
            saved_object.obj.video = Video.objects.get(id = bundle.data['video'])
            saved_object.obj.save()
            return saved_object
        return bundle
    
    
    def obj_update(self, bundle, request = None, **kwargs):
        note = None
        if bundle.data is not None:
            note = Note.objects.get( id = bundle.data['id'] )
            if note is not None:
                if note.user == request.user or note.video.user == request.user:
                    self.strip_bundle_data(bundle)
                    return_val = super(NoteResource, self).obj_update(bundle, request, **kwargs)
                    return return_val
                else:
                    raise ImmediateHttpResponse(response=http.HttpUnauthorized())
                    #raise PermissionDenied("User Doesn't have permission to edit this note.")
            
        return Bundle(obj = note)
    
    
    def obj_delete(self, request=None, **kwargs):
        
        obj = kwargs.pop('_obj', None)

        if not hasattr(obj, 'delete'):
            try:
                obj = self.obj_get(request, **kwargs)
            except ObjectDoesNotExist:
                raise NotFound("A model instance matching the provided arguments could not be found.")
        
        if obj is not None:
            if obj.user == request.user or obj.video.user == request.user:
                return_val = super(NoteResource, self).obj_delete(request, **kwargs)
            else:
                raise ImmediateHttpResponse(response=http.HttpUnauthorized())
                #raise PermissionDenied("User Doesn't have permission to delete this note.")
    
    
    
    
    def get_object_list(self, request):
        return get_user_visible_objects(Note, request)
    
        
    
    #TODO: Searching notes
    #TODO: Filter by limits?
    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(NoteResource, self).build_filters(filters)

        if "q" in filters:
            pass

        return orm_filters
    
    
    def save_related(self, bundle):
        pass
    def obj_delete_list(self, request=None, **kwargs):
        pass
    
    
    #Theoretically removes any JS injections.
    def strip_bundle_data(self, bundle):
        bundle.data['text'] = strip(str(bundle.data.get('text', '')))
        bundle.data['user_name'] = strip(str(bundle.data.get('user_name', '')))
        bundle.data['icon_link'] = strip(str(bundle.data.get('icon_link', '')))
        bundle.data['source'] = strip(str(bundle.data.get('source', '')))
        bundle.data['source_link'] = strip(str(bundle.data.get('source_link', '')))
        bundle.data['type'] = strip(str(bundle.data.get('type', '')))
        bundle.data['original_source'] = strip(str(bundle.data.get('original_source', '')))
        bundle.data['original_source_link'] = strip(str(bundle.data.get('original_source_link', '')))
        #del(bundle.data['original_data'])
        return bundle
        
        
        
        
    class Meta:
        queryset = Note.published_objects.all()
        resource_name = "note"
        filtering = {
            'video': ALL_WITH_RELATIONS,
            'time': ['gt', 'gte', 'lt', 'lte',]
        }
        ordering = ['offset', 'time', 'end_time', 'creation_time',]
        list_allowed_methods = ['get', 'post', ]
        detail_allowed_methods = ['get', 'post', 'put', 'patch', 'delete']
        always_return_data = True
        authentication = Authentication()
        authorization = DjangoAuthorization()
        
 
 
 
 
 
 
 
class SourceResource(ModelResource):
    
    user = fields.ToOneField('core.api.resources.UserResource', 'user', full = True, null = True, blank = True)
    video = fields.ToOneField('core.api.resources.VideoResource', 'video', null = True, blank = True)
    published = fields.BooleanField('published', default = True, readonly = True)
    creation_time = fields.DateField(attribute = 'creation_time', readonly = True)
    update_time  = fields.DateField(attribute = 'update_time', readonly = True)
    
    '''
    So it appears that related models don't get saved. (As in, a video id won't be converted to the right video.)
    So ratehr than dealing with the default bundle saving, I'm just creating a new note and saving it myself.
    '''
    def obj_create(self, bundle, request=None, **kwargs):
        if bundle.data is not None:
            bundle.data['url'] = strip(bundle.data.get('url', ''))
            bundle.data['type'] = strip(bundle.data.get('type', ''))
            bundle.data['twitter_user'] = strip(bundle.data.get('twitter_user', ''))
            bundle.data['twitter_start_id'] = strip(bundle.data.get('twitter_start_id', ''))
            bundle.data['twitter_end_id'] = strip(bundle.data.get('twitter_end_id', ''))
            bundle.data['twitter_search'] = strip(bundle.data.get('twitter_search', ''))
            bundle.data['twitter_hash'] = strip(bundle.data.get('twitter_hash', ''))
            kwargs['video'] = Video.objects.get(id = bundle.data['video_id'])
            kwargs['user'] = request.user
            kwargs['user_name'] = request.user.username
            
        return super(SourceResource, self).obj_create(bundle, request, **kwargs)
    
    
    def save_related(self, bundle):
        pass
    def obj_delete_list(self, request=None, **kwargs):
        pass
    
    class Meta:
        queryset = Source.objects.all()
        resource_name = "source"
        filtering = {
            'video': ALL_WITH_RELATIONS,
            'time': ['gt', 'gte', 'lt', 'lte',]
        }
        ordering = ['update_time',]
        list_allowed_methods = ['get', 'post', ]
        detail_allowed_methods = ['get', 'post', 'put', 'patch',]
        always_return_data = True
        authentication = Authentication()
        authorization = DjangoAuthorization()
 
 
 
 
        
        
class UserResource(ModelResource):
    
    
    # Would like to find a way to only include these if loading a User directly.
    # Annoying that they come back on a request for every note / video.
    
    #videos = fields.ToManyField(VideoResource, 'video_set')
    #notes  = fields.ToManyField(NoteResource, 'note_set')
    
    def obj_update(self, bundle, request = None, **kwargs):
        '''
        I somehow got an entire user wiped, because an update on a video had mostly blank user content (whitelisted fields).
        This is weird because I'm only allowing 'get' here. It's clearly being populated from a save from the video. Ugh.
        
        I don't want anything to change.
        
        '''
        
        if bundle.data['id'] is None:
            return bundle
        
        user = User.objects.get(id = bundle.data['id'])
        bundle.data = user
        
        return bundle
    
    class Meta:
        queryset = User.objects.all()
        list_allowed_methods = ['get',]
        detail_allowed_methods = ['get',]
        always_return_data = True
        authentication = Authentication()
        authorization = DjangoAuthorization()
        include_resource_uri = False
        #important. Let's just whitelist what we need.
        fields = ['id', 'username', 'first_name', 'last_name',]
        
 
 
 
 
 
 
 
 
 
 
def get_user_visible_objects(model, request):
    #first, figure out if the user should see unpublished objects
    qs = model.published_objects
    if request.user.is_authenticated() and request.user.is_staff:
        qs = model.objects
    
    #now exclude the items where the private is marked AND aren't from this user
    qs = qs.exclude( Q(private = True) & ~Q(user__id = request.user.id) )
    return qs        
    