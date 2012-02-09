from tastypie import fields
from tastypie.bundle import Bundle
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS, ALL
from tastypie.authentication import Authentication
from tastypie.authorization import DjangoAuthorization
from core.models import *
from core.helpers.strip_tags import strip
from datetime import datetime, timedelta
from django.db import connection
from django.contrib.auth.models import User
from tastypie.exceptions import NotFound, ImmediateHttpResponse
from django.core.exceptions import PermissionDenied
from tastypie import http

         


class VideoResource(ModelResource):
    #I guess it should be expected that the user first grabs the video, gets the id, and then grabs the notes.
    #neither have to know about the other.
    #notes = fields.ToManyField('core.api.resources.NoteResource', 'note_set')
    user = fields.ToOneField('core.api.resources.UserResource', 'user', full = True, null = True, blank = True)
    
    def obj_create(self, bundle, request = None, **kwargs):
        if bundle.data is not None:
            bundle.data['title'] = strip(bundle.data['title'])
            bundle.data['description'] = strip(bundle.data['description'])
            bundle.data['user'] = request.user
            bundle.data['user_name'] = request.user.username
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
        
        if bundle.data is not None:
            video = Video.objects.get( id = bundle.data['id'] )
            if video is not None and video.user == request.user:
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
    
    user = fields.ToOneField('core.api.resources.UserResource', 'user', full = True, null = True, blank = True)
    
    
    
    '''
    So it appears that related models don't get saved. (As in, a video id won't be converted to the right video.)
    So ratehr than dealing with the default bundle saving, I'm just creating a new note and saving it myself.
    '''
    def obj_create(self, bundle, request=None, **kwargs):
        if bundle.data is not None:
            self.strip_bundle_data(bundle)
            kwargs['video'] = Video.objects.get(id = bundle.data['video'])
            kwargs['user'] = request.user
            kwargs['user_name'] = request.user.username
            kwargs['source'] = 'tv'
        return super(NoteResource, self).obj_create(bundle, request, **kwargs)
    
    
    
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
        bundle.data['text'] = strip(bundle.data.get('text', ''))
        bundle.data['user_name'] = strip(bundle.data.get('user_name', ''))
        bundle.data['icon_link'] = strip(bundle.data.get('icon_link', ''))
        bundle.data['source'] = strip(bundle.data.get('source', ''))
        bundle.data['source_link'] = strip(bundle.data.get('source_link', ''))
        bundle.data['type'] = strip(bundle.data.get('type', ''))
        bundle.data['original_source'] = strip(bundle.data.get('original_source', ''))
        bundle.data['original_source_link'] = strip(bundle.data.get('original_source_link', ''))
        bundle.data['original_data'] = ''
        return bundle
        
        
        
        
    class Meta:
        queryset = Note.objects.all()
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
        
        
    