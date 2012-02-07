from django.db import models
from django.template.defaultfilters import slugify
#users
from django.contrib.auth.models import User
from datetime import datetime, timedelta
#tags
from taggit_autosuggest.managers import TaggableManager
from taggit.models import GenericTaggedItemBase, TagBase
from django.db.models.signals import post_save


class PublishedManager(models.Manager):
    def get_query_set(self):
        return super(PublishedManager, self).get_query_set().filter(published = True)


class CommonInfo(models.Model):
    published       = models.BooleanField(default = True)
    tags            = TaggableManager(blank = True, through='CustomTagItem')
    creation_time   = models.DateTimeField() # generated in save, time this object is created
    update_time     = models.DateTimeField(blank = True, null = True) # generated in save, time this object is updated
    time            = models.DateTimeField(null = True, blank = True) # time that content applies to.
    end_time        = models.DateTimeField(null = True, blank = True) #UTC time content ends (if applicable)
    
    
    objects = models.Manager()
    published_objects = PublishedManager()
    
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
    ('youtube','YouTube'),
    ('mp4','mp4'),
    ('flv','flv'),
    ('3gp','3gp'),
)


SOURCE_TYPE_CHOICES = (
    ('twitter','Twitter'),
    ('storify','Storify'),
    ('coveritlive','Cover It Live'),
    ('scribblelive','ScribbleLive'),
    ('csv', 'CSV'),
#    ('fark','Fark.com'),
)




class Video(CommonInfo):
    title           = models.CharField(max_length=256, blank=True,  verbose_name = 'Name or Title')
    slug            = models.SlugField(max_length=256, blank=False, unique=True)
    description     = models.TextField(blank=False)
    teaser          = models.TextField(blank = True)
    user            = models.ForeignKey(to=User, blank = True, null = True) #allow anonymous uploads?
    type            = models.CharField(max_length = 32, blank = True, choices = VIDEO_TYPE_CHOICES, default='mp4')
    video_length    = models.IntegerField(null = True, default = 0) #Length in seconds.
    '''
         Do we want duplicate videos, or do we want to limit the system to handle only one of each youtube id?
         In the future maybe we want to alert the user that the video is already in the system and give them a choice? This is an annoying problem.
    '''
    video_url       = models.CharField(max_length = 256,  blank = True, verbose_name = "Path to source video or YouTube ID", unique = True)
    #do we just take the video url and set it to video file if upload?
    video_file      = models.FileField(upload_to='viodeotext/contrib/videos/', null=True, blank=True)
    user_name       = models.CharField(max_length = 64, blank = True) # if not a user in the system, just a name
    user_link       = models.URLField(blank = True, verify_exists = False) # if the user has a link.
    icon            = models.ImageField(upload_to='videotext/contrib/icons/', null=True, blank=True) # image icon if uploaded
    icon_link       = models.URLField(blank = True, verify_exists = False) # image icon if on another server, ie YouTube Screenshot
    private         = models.BooleanField(default = False) #if for some reason we want to make this accessible only ot "user"
    lock_notes      = models.BooleanField(default = False) #stops notes from being added -- should only work on uploaded videos.
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify("{0} {1}".format(self.title, datetime.now().strftime('%m-%d-%Y-%H-%M-%S') ))
        
        #getting an error: can't subtract offset-naive and offset-aware datetimes -- may not be worth it to solve.
        #if (self.time != None) and (self.end_time != None):
                #self.video_length = (self.end_time - self.time).seconds     
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
    
    #just a convienience...
    @property
    def all_notes(self):
        return self.note_set.all()
    
    
    
    @models.permalink
    def get_absolute_url(self):
        return ('video_view', (), {'slug': self.slug})
    
    def __unicode__(self):
        return u'Video: %s' % (self.title)



'''
Places to pull in content from when creating a video.
'''
class Source(CommonInfo):
    url       = models.URLField(max_length = 512, blank = True, verify_exists = False)
    type      = models.CharField(max_length = 32, blank = False, choices = SOURCE_TYPE_CHOICES, default = 'twitter')
    video     = models.ForeignKey(to = "Video", blank = False, null = True)
    user      = models.ForeignKey(to=User, blank = True, null = True)
    scraped   = models.BooleanField(default = False, verbose_name = 'Data Scraped')
    # Either we save scraped content here as a zip file or text file or whatever
    # OR we let people upload a CSV in a specific format to parse for notes.
    content   = models.FileField(upload_to = 'tvn/contrib/source_data/', null = True, blank = True, verbose_name = 'Content Location')
    
    
    def save(self, *args, **kwargs):
        
        from parsers.scribblelive import parse_scribbling
        from parsers.storify import parse_storify
        from parsers.fark import parse_fark
        #save first so we at least have an id?
        if not self.id:
            super(Source, self).save(*args, **kwargs)
        
        if self.video and self.url and not self.scraped:
            try:
                if self.type == "twitter":
                    pass
                elif self.type == "storify":
                    parse_storify(self.url, self.video)
                elif self.type == "coveritlive":
                    pass
                elif self.type == "scribblelive":
                    parse_scribbling(self.url, self.video)
                elif self.type == "csv":
                    pass
                elif self.type == "fark":
                    parse_fark(self.url, self.video)
                self.scraped = True
            except Exception:
                self.scraped = False
            
        
        super(Source, self).save(*args, **kwargs)





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
    source_link = models.CharField(max_length = 512, blank = True,  null = True) #could be absolute URL or path.
    source      = models.CharField(max_length = 256, blank = True, null=True)
    offset      = models.IntegerField(null = True, blank = True) # position within video in seconds.
    private     = models.BooleanField(default = False)
    
    
    def save(self, *args, **kwargs):
        #if we don't have an id, save to get one.
        if not self.id:
            super(Note, self).save(*args, **kwargs)
            
        
        if self.video != None:
            if (self.time != None) and (self.video.time != None):  #If we have the times, calculate offset, otherwise assume it's passed in.
                    self.offset = self.gen_offset
            
            if (self.time == None) and (self.video.time != None) and (self.offset != None):
                self.time = self.video.time + timedelta(seconds = self.offset)
        
            self.link = '{0}#note/{1}'.format(self.video.get_absolute_url(), self.id) 
        
        #Get or create sets force_insert = True. Which causes this to bomb on parser inputs. Lets stop that.
        kwargs['force_insert'] = False
        super(Note, self).save(*args, **kwargs)
        
            
    
    @property
    def gen_offset(self):
        #I'm sure there's a more concise way to do this, but timedeltas, man.
        delta = self.time - self.video.time
        if self.time < self.video.time:
            delta = self.video.time - self.time
            return delta.seconds * -1 
        return delta.seconds
    
    
    
    def __unicode__(self):
        return u'Note: %s' % (self.text)
    
    class Meta:
        ordering = ['time', 'end_time', 'creation_time']
    









#hold extra metadata for user
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    accepted_eula = models.BooleanField(default = False)
    can_note = models.BooleanField(default = False)
    role = models.CharField(max_length = 32, blank = True, null = True, default = 'user')


#creates profile when User created
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user = instance)
#post_save.connect(create_user_profile, sender = User)




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