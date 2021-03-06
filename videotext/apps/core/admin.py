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
    list_display = ('title', 'video_url', 'published', 'type', 'private', 'user',)
    list_editable= ('published',)
    list_display_links = ('title',)




class SourceAdmin(CommonAdmin):
    fieldsets = (
        ('The Basics',
            {
                'fields': ('name', 'user', 'video', 'url', 'type', 'scraped', 'content',)
            }
        ),
        ('Twitter Specific',
            {
                'fields': ('twitter_user', 'twitter_hash', 'twitter_start_id', 'twitter_end_id', 'twitter_search',)
            }
        ),
        ('CSV Specific',
            {
                'fields': ('csv_data',)
            }
        ),
        ('SRT Specific',
            {
                'fields': ('srt_data',)
            }
        ),
        ('Oops',
            {
                'fields': ('error_message',)
            }
        )
    )
    
    list_display = ('name', 'url', 'video', 'creation_time', 'type')
    list_display_links = ('name', 'url', 'video', 'creation_time', 'type',)
    readonly_fields = ('csv_data', 'srt_data',)




class NoteAdmin(CommonAdmin):
    fieldsets = (
        ('The Basics',
            {
                'fields': ('text', 'user', 'video', 'published', 'tags', 'private',)
            }
        ),
        ('The Details',
            {
                'fields': ('time', 'end_time', 'offset', 'end_offset', 'user_name', 'user_link', 'link', 'icon_link', 'icon', 'type',
                           'source', 'source_link', 'original_source', 'original_source_link', 'import_source', 'import_source_name',)
            }
        ),
    )
    
    list_display = ('text', 'video', 'offset', 'published',)
    list_editable= ('published',)
    list_display_links = ('text',)
    list_filter = ('published', 'private', 'video', 'user', 'import_source', 'type',)
    search_fields = ('text',)
    readonly_fields = ('import_source_name',)



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





#admin.site.unregister(User)
#
#class UserProfileInline(admin.TabularInline):
#    model = UserProfile
#
#class UserAdmin(admin.ModelAdmin):
#    inlines = [UserProfileInline]
#
#admin.site.register(User, UserAdmin)

#select setval('contracts_id_seq', (select max(id) + 1 from contracts));



admin.site.register(Video, VideoAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(UserProfile, UserProfileAdmin)