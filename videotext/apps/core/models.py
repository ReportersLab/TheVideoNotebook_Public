from django.db import models
from django.template.defaultfilters import slugify
#users
from django.contrib.auth.models import User
from datetime import datetime
#tags
from taggit_autosuggest.managers import TaggableManager
from taggit.models import GenericTaggedItemBase, TagBase


class PublishedManager(models.Manager):
    def get_query_set(self):
        return super(PublishedManager, self).get_query_set().filter(published = True)


class CommonInfo(models.Model):
    published       = models.BooleanField(default = True)
    tags            = TaggableManager(blank = True, through='CustomTagItem')
    creation_time   = models.DateTimeField() # generated in save, time this object is created
    update_time     = models.DateTimeField() # generated in save, time this object is updated
    time            = models.DateTimeField() # UTC time that content applies to.
    end_time        = models.DateTimeField(null = True, blank = True) #UTC time content ends (if applicable)
    
    
    objects = PublishedManager()
    all_objects = models.Manager()
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.creation_time = datetime.now()
        self.update_time = datetime.now()
        super(CommonInfo, self).save(*args, **kwargs)
        
    
    @property
    def verbose_name(self):
        return self._meta.verbose_name
    
    class Meta:
        abstract = True
        ordering = ['-creation_time',] #this doesn't seem to work for abstract models.




VIDEO_TYPE_CHOICES = (
    ('youtube','youtube'),
    ('mp4','mp4'),
    ('flv','flv'),
    ('3gp','3gp'),
)




class Video(CommonInfo):
    title           = models.CharField(max_length=256, blank=True,  verbose_name = 'Name or Title')
    slug            = models.SlugField(max_length=256, blank=False, unique=True)
    description     = models.TextField(blank=False)
    teaser          = models.TextField(blank = True)
    user            = models.ForeignKey(to=User, blank = True, null = True) #allow anonymous uploads?
    type            = models.CharField(max_length = 32, blank = True, choices = VIDEO_TYPE_CHOICES, default='mp4')
    #Will want to verify this exists in the future
    video_url       = models.URLField(max_length = 256,  blank = False, verbose_name = "Path to source video", verify_exists = False)
    #do we just take the video url and set it to video file if upload?
    video_file      = models.FileField(upload_to='viodeotext/contrib/videos/', null=True, blank=True)
    
    user_name       = models.CharField(max_length = 64, blank = True) # if not a user in the system, just a name
    user_link       = models.URLField(blank = True, verify_exists = False) # if the user has a link.
    icon            = models.ImageField(upload_to='videotext/contrib/icons/', null=True, blank=True) # image icon if uploaded
    icon_link       = models.URLField(blank = True, verify_exists = False) # image icon if on another server, ie YouTube Screenshot
    
    
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify("{0} {1}".format(self.title, self.time.date().isoformat()))
        super(Video, self).save(*args, **kwargs)
    
    
    @property
    def length(self):
        #calculate video length. May want to convert this to seconds or something.
        return self.end_time - self.time 
    
    @property
    def pre_event_notes(self):
        return self.note_set.filter(time__lt = self.time)
        
    @property
    def event_notes(self):
        return self.note_set.filter(time__gte = self.time).filter(time__lte = self.end_time)
    
    @property
    def post_event_notes(self):
        return self.note_set.filter(time__gt = self.end_time)
        
    
    
    
    @models.permalink
    def get_absolute_url(self):
        return ('video_view', (), {'slug': self.slug})
    
    def __unicode__(self):
        return u'Video: %s' % (self.title)



class Note(CommonInfo):
    text        = models.TextField(blank = False) #cover-it-live and live blogs may have much longer posts.
    user        = models.ForeignKey(to = User, blank = True, null = True) # if a user is annotating a video
    user_name   = models.CharField(max_length = 64, blank = True, null = True) # if not a user in the system, just a name
    user_link   = models.URLField(max_length = 512, blank = True, verify_exists = False, null = True) # if the user has a link.
    video       = models.ForeignKey(to = "Video", blank = False, null = True) # related video. Shouldn't be null, but null for testing.
    link        = models.URLField(max_length = 512, blank = True, verify_exists = False, null = True) #link to original comment -- ie, a Tweet
    icon        = models.ImageField(upload_to='videotext/contrib/icons/', null=True, blank=True) # image icon if uploaded
    icon_link   = models.URLField(max_length = 512, blank = True, verify_exists = False, null = True) # image icon if on another server, ie Twitter User Photo
    type        = models.CharField(max_length = 32, blank = True, null = True)
    source_link = models.URLField(max_length = 512, blank = True, verify_exists = False, null = True)
    source      = models.CharField(max_length = 256, blank = True, null=True)
    
    
    
    @property
    def offset(self):
        delta = self.time - self.video.time
        return delta.seconds
    
    
    
    def __unicode__(self):
        return u'Note: %s' % (self.text)
    
    class Meta:
        ordering = ['time', 'end_time', 'creation_time']
    





class CustomTag(TagBase):
    
    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(CustomTag, self).save(*args, **kwargs)
        
    
    @models.permalink
    def get_absolute_url(self, slug):
        return ('tag_view', (), {'slug': self.slug})
    
    
    def clean_name(self):
        out = self.name
        try:
            out = self.name.split(':')[1]
        except IndexError:
            pass
        
        return out
    
    def style_name(self):
        out = ''
        try:
            out = self.name.split(':')[0]
        except IndexError:
            pass
        return out
        
    class Meta:
        verbose_name = "Kitchen Tag"
        verbose_name_plural = "Kitchen Tags"


class CustomTagItem(GenericTaggedItemBase):
    tag = models.ForeignKey(CustomTag, related_name="tagged_items")