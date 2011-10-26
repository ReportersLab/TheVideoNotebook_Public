from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from models import Video, Note, UserProfile
from django.contrib import admin




class CommonAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    save_on_top = True
    list_filter = ('published',)
    
    
    #def view_link(self, object):
    #    return '<a href="{0}">{0}</a>'.format(object.get_absolute_url())
    #view_link.allow_tags = True
    
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        #if it's one of our custom models -- which currently all have an all_objects property
        #return all objects
        try:
            kwargs['queryset'] = db_field.rel.to.all_objects
        except AttributeError:
            pass
        #otherwise, return the normal content.
        return super(CommonAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        try:
            kwargs['queryset'] = db_field.rel.to.all_objects
        except AttributeError:
            pass
        return super(CommonAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
        
    
    def queryset(self, request):
        # In the Admin we want to get all objects, not just published ones.
        return self.model.all_objects
        #this is the normal implementation
        #return super(CommonAdmin, self).queryset(request)
    
    
    class Media:
        js = (settings.STATIC_URL+'grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js', settings.STATIC_URL+'js/tinymce_setup.js')




class VideoAdmin(CommonAdmin):
    fieldsets = (
        ('The Basics',
            {
                'fields': ('title', 'type', 'teaser', 'description', 'user', 'published', 'tags', 'slug',)
            }
        ),
        ('The Details',
            {
                'fields': ('video_url', 'video_file', 'time', 'end_time', 'video_length', 'user_name', 'user_link', 'icon', 'icon_link',)
            }
        ),
    )
    readonly_fields = ('slug',)
    list_display = ('title', 'video_url', 'published', 'type',)
    list_editable= ('published',)
    list_display_links = ('title',)




class NoteAdmin(CommonAdmin):
    fieldsets = (
        ('The Basics',
            {
                'fields': ('text', 'user', 'video', 'published', 'tags', )
            }
        ),
        ('The Details',
            {
                'fields': ('time', 'end_time', 'offset', 'user_name', 'user_link', 'link', 'icon_link', 'icon', 'type', 'source_link', 'source',)
            }
        ),
    )
    
    list_display = ('text', 'video', 'published',)
    list_editable= ('published',)
    list_display_links = ('text',)



class UserProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ('The Basics',
            {
                'fields': ('user', 'role', 'can_note', 'accepted_eula', )
            }
        ),
    )
    
    list_display = ('user', 'role', 'can_note',)
    list_editable= ('can_note',)
    list_display_links = ('user',)





admin.site.register(Video, VideoAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(UserProfile, UserProfileAdmin)