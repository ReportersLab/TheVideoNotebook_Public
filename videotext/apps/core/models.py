from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify
from taggit_autosuggest.managers import TaggableManager
from taggit.models import GenericTaggedItemBase, TagBase
import pytz


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
    ('mp3','mp3'),
)


SOURCE_TYPE_CHOICES = (
    ('twitter','Twitter'),
    ('storify','Storify'),
#    ('coveritlive','Cover It Live'),
    ('scribblelive','ScribbleLive'),
    ('csv', 'CSV'),
    ('granicus', 'Granicus'),
#    ('fark','Fark.com'),
    ('srt', 'SRT Captions (YouTube)'),
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
    video_file      = models.FileField(upload_to='tvn/contrib/videos/', null=True, blank=True, max_length = 512)
    user_name       = models.CharField(max_length = 64, blank = True) # if not a user in the system, just a name
    user_link       = models.URLField(blank = True, verify_exists = False) # if the user has a link.
    icon            = models.ImageField(upload_to='tvn/contrib/icons/', null=True, blank=True, max_length = 512) # image icon if uploaded
    icon_link       = models.URLField(blank = True, verify_exists = False) # image icon if on another server, ie YouTube Screenshot
    private         = models.BooleanField(default = False) #if for some reason we want to make this accessible only ot "user"
    lock_notes      = models.BooleanField(default = False) #stops notes from being added -- should only work on uploaded videos.
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify("{0} {1}".format(self.title, datetime.now().strftime('%m-%d-%Y-%H-%M-%S') ))
        
        #if self.icon is not None:
        #    self.icon_link = 'http://{0}/{1}'.format(settings.AWS_STORAGE_BUCKET_NAME, self.icon)
        if not self.time:
            self.time = datetime.now()
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
    name                 = models.CharField(max_length = 128, blank = True, null = True)
    url                  = models.URLField(max_length = 512, blank = True, verify_exists = False)
    type                 = models.CharField(max_length = 32, blank = False, choices = SOURCE_TYPE_CHOICES, default = 'twitter')
    video                = models.ForeignKey(to = "Video", blank = False, null = True)
    user                 = models.ForeignKey(to=User, blank = False, null = False)
    scraped              = models.BooleanField(default = False, verbose_name = 'Data Scraped')
    #twitter specific stuff
    twitter_user         = models.CharField(max_length = 32, blank = True, null = True)
    twitter_hash         = models.CharField(max_length = 64, blank = True, null = True)
    twitter_start_id     = models.CharField(max_length = 128, blank = True, null = True)
    twitter_end_id       = models.CharField(max_length = 128, blank = True, null = True)
    twitter_search       = models.CharField(max_length = 256, blank = True, null = True) #possibly a search string to attack Twitter with
    #silly attempt to get around no file-upload support in TastyPie. Just paste the CSV!
    csv_data             = models.TextField(blank = True, null = True)
    #same silly attempt for SRT data.
    srt_data             = models.TextField(blank = True, null = True, help_text = "Caption Data in the SRT Format, YouTube uses this.")
    
    # Either we save scraped content here as a zip file or text file or whatever
    # OR we let people upload a CSV in a specific format to parse for notes.
    content   = models.FileField(upload_to = 'tvn/contrib/source_data/', null = True, blank = True, verbose_name = 'Content Location')
    error_message = models.CharField(max_length = 256, null = True, blank = True)
    
    def __unicode__(self):
        if self.type == 'twitter':
            return 'Source: @%s, %s to %s (scraped: %s)' % (self.twitter_user, self.twitter_start_id, self.twitter_end_id, self.scraped)
        return 'Source: %s -- %s (scraped: %s)' % (self.url, self.type, self.scraped)
    
    @property
    def description(self):
        if self.name:
            return self.name
        if self.type == 'twitter':
            return 'Source: @%s, %s to %s' % (self.twitter_user, self.twitter_start_id, self.twitter_end_id)
        return 'Source: %s -- %s' % (self.url, self.type)
    
    
    def save(self, *args, **kwargs):
        
        from parsers.scribblelive import parse_scribbling
        from parsers.storify import parse_storify
        from parsers.fark import parse_fark
        from parsers.tvncsv import import_tvn_csv
        from parsers.twitterparser import get_tweets
        from parsers.granicus import get_granicus_data
        from parsers.srt import get_srt_data
        #save first so we at least have an id?
        if not self.id:
            super(Source, self).save(*args, **kwargs)
        
        #twitter IDs may be send in as URLs to the post. The id is the last portion of that.
        self.twitter_start_id = self.twitter_start_id.split('/')[-1]
        self.twitter_end_id = self.twitter_end_id.split('/')[-1]
        self.twitter_hash = self.twitter_hash.replace('#', '')
        self.twitter_user = self.twitter_user.replace('@', '')
        
        if self.video and (self.url or self.content or (self.type == 'twitter') or self.csv_data or self.srt_data) and not self.scraped:
            try:
                if self.type == "twitter":
                    get_tweets(self)
                elif self.type == "storify":
                    parse_storify(self.url, self.video, import_source = self)
                elif self.type == "coveritlive":
                    pass
                elif self.type == "scribblelive":
                    parse_scribbling(self.url, self.video, import_source = self)
                elif self.type == "csv":
                    import_tvn_csv(self)
                elif self.type == "fark":
                    parse_fark(self.url, self.video, import_source = self)
                elif self.type == 'granicus':
                    get_granicus_data(self)
                elif self.type == 'srt':
                    get_srt_data(self)
                    
                self.scraped = True
                self.error_message = ''
            except Exception as e:
                self.error_message = '{0}'.format(e)
                self.scraped = False
        
        
        super(Source, self).save(*args, **kwargs)





class Note(CommonInfo):
    text                    = models.TextField(blank = False) #cover-it-live and live blogs may have much longer posts.
    user                    = models.ForeignKey(to = User, blank = True, null = True) # if a user is annotating a video
    user_name               = models.CharField(max_length = 64, blank = True, null = True) # if not a user in the system, just a name
    user_link               = models.URLField(max_length = 512, blank = True, verify_exists = False, null = True) # if the user has a link.
    video                   = models.ForeignKey(to = "Video", blank = False, null = True) # related video. Shouldn't be null, but null for testing.
    link                    = models.CharField(max_length = 512, blank = True, null = True) #link to original comment -- ie, a Tweet
    icon                    = models.ImageField(upload_to='videotext/contrib/icons/', null=True, blank=True) # image icon if uploaded
    icon_link               = models.URLField(max_length = 512, blank = True, verify_exists = False, null = True) # image icon if on another server, ie Twitter User Photo
    type                    = models.CharField(max_length = 32, blank = True, null = True)
    source_link             = models.CharField(max_length = 512, blank = True,  null = True) #could be absolute URL or path.
    source                  = models.CharField(max_length = 256, blank = True, null = True) #string describing the source
    original_source         = models.CharField(max_length = 256, blank = True, null = True) #if the source pulls content from elsewhere -- see Storify
    original_source_link    = models.URLField(max_length = 512, blank = True, verify_exists = False, null = True)
    offset                  = models.IntegerField(null = True, blank = True) # position within video in seconds.
    end_offset              = models.IntegerField(null = True, blank = True) # end position of video in seconds (for captions?)
    private                 = models.BooleanField(default = False) 
    original_data           = models.TextField(blank = True, null = True) #would like to store the original HTML or JSON block here.
    import_source           = models.ForeignKey(to = Source, blank = True, null = True, verbose_name = 'Import Data Source')
    
    def save(self, *args, **kwargs):
        #if we don't have an id, save to get one.
        if not self.id:
            super(Note, self).save(*args, **kwargs)
            
        if self.video != None:
            if (self.time != None) and (self.video.time != None):  #If we have the times, calculate offset, otherwise assume it's passed in.
                    self.offset = self.gen_offset()
            
            if (self.time == None) and (self.video.time != None) and (self.offset != None):
                self.time = self.video.time + timedelta(seconds = self.offset)
                
            self.link = '{0}#note/{1}'.format(self.video.get_absolute_url(), self.id) 
        
        #Get or create sets force_insert = True. Which causes this to bomb on parser inputs. Lets stop that.
        kwargs['force_insert'] = False
        super(Note, self).save(*args, **kwargs)
    
    
    def gen_offset(self):
        # Make sure both times have a timezone so we can do math.
        # I'm honestly not sure if we can even save this data to make this unnecessary.
        # I think what's happening is that the Note being saved comes from TastyPie and
        # has a TZ, but the Video doesn't (because it's unsavable). The math then explodes.
        django_tz = pytz.timezone(settings.TIME_ZONE)
        if self.video.time.tzinfo is None:
            self.video.time = django_tz.localize(self.video.time)
        if self.time.tzinfo is None:
            self.time = django_tz.localize(self.time)
            
        #I'm sure there's a more concise way to do this, but timedeltas, man.
        delta = self.time - self.video.time
        if self.time < self.video.time:
            delta = self.video.time - self.time
            #return delta.total_seconds() * -1
            #server is python 2.6, no total_seconds property. Should probably update at some point.
            return ((delta.microseconds + (delta.seconds + delta.days * 24 * 3600) * 10**6) / 10**6) * -1
        return ((delta.microseconds + (delta.seconds + delta.days * 24 * 3600) * 10**6) / 10**6)
    
    
    
    def __unicode__(self):
        return u'Note: %s' % (self.text)
    
    class Meta:
        ordering = ['time', 'end_time', 'creation_time']
    







'''
None of this is actually implemented yet. The idea would be to create some sort of user creation system in the future.
The users would need some metadata in addition to the standard Djagno info, and we would put it here (this is how the
Django docs recommend doing it.) 
'''

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