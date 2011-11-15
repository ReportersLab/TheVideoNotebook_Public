from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from models import Video, Note, UserProfile, Source
from django.contrib import admin




class CommonAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    save_on_top = True
    list_filter = ('published',)
    
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
                'fields': ('video_url', 'video_file', 'time', 'end_time', 'video_length', 'user_name',
                           'user_link', 'icon', 'icon_link', 'private', 'lock_notes',)
            }
        ),
    )
    readonly_fields = ('slug',)
    list_display = ('title', 'video_url', 'published', 'type',)
    list_editable= ('published',)
    list_display_links = ('title',)




class SourceAdmin(CommonAdmin):
    fieldsets = (
        ('The Basics',
            {
                'fields': ('user', 'video', 'url', 'type',)
            }
        ),
    )
    
    list_display = ('url', 'video', 'creation_time',)
    list_display_links = ('url',)




class NoteAdmin(CommonAdmin):
    fieldsets = (
        ('The Basics',
            {
                'fields': ('text', 'user', 'video', 'published', 'tags', 'private',)
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
admin.site.register(Source, SourceAdmin)
admin.site.register(UserProfile, UserProfileAdmin)