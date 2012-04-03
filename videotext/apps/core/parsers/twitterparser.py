import twitter
from django.conf import settings
from core.models import Note, Video
from datetime import datetime



def get_tweets(source = None):
    #eventually we need some system of letting a user log in and get their own access token key and secret
    #for now we use the @reporterslab account.
    api = twitter.Api(consumer_key=settings.TWITTER_CONSUMER_KEY, consumer_secret=settings.TWITTER_CONSUMER_SECRET,
                      access_token_key=settings.TWITTER_ACCESS_TOKEN, access_token_secret=settings.TWITTER_TOKEN_SECRET)
    
    
    statuses = api.GetUserTimeline(screen_name = source.twitter_user, count = 200,
                                   since_id=(int(source.twitter_start_id) - 1), max_id=source.twitter_end_id, include_entities = True, include_rts = True )
    
    
    for tweet in statuses:
        #by default add all notes
        add_note = True    
        #but if there's a hash tag, only add notes with the appropriate hash
        if source.twitter_hash:
            add_note = False
            for hash in tweet.hashtags:
                if hash.text.lower() == source.twitter_hash.lower():
                    add_note = True
        
        
        if add_note:
            note, created = Note.objects.get_or_create(
                                    text = tweet.text,
                                    time = datetime.fromtimestamp(tweet.created_at_in_seconds),
                                    user = source.user,
                                    user_name = tweet.user.screen_name,
                                    source = 'Twitter',
                                    source_link = 'https://twitter.com/#!/{0}/status/{1}'.format(tweet.user.screen_name, tweet.id),
                                    original_source = tweet.source,
                                    icon_link = tweet.user.profile_image_url,
                                    type = 'twitter',
                                    original_data = tweet.AsJsonString(),
                                    video = source.video,
                                    import_source = source,
                            )
        








'''
  status.created_at
  status.created_at_in_seconds # read only
  status.favorited
  status.in_reply_to_screen_name
  status.in_reply_to_user_id
  status.in_reply_to_status_id
  status.truncated
  status.source
  status.id
  status.text
  status.location
  status.relative_created_at # read only
  status.user
  status.urls
  status.user_mentions
  status.hashtags
'''
'''
   text                    = models.TextField(blank = False) #cover-it-live and live blogs may have much longer posts.
    user                    = models.ForeignKey(to = User, blank = True, null = True) # if a user is annotating a video
    user_name               = models.CharField(max_length = 64, blank = True, null = True) # if not a user in the system, just a name
    user_link               = models.URLField(max_length = 512, blank = True, verify_exists = False, null = True) # if the user has a link.
    video                   = models.ForeignKey(to = "Video", blank = False, null = True) # related video. Shouldn't be null, but null for testing.
    link                    = models.URLField(max_length = 512, blank = True, verify_exists = False, null = True) #link to original comment -- ie, a Tweet
    icon                    = models.ImageField(upload_to='videotext/contrib/icons/', null=True, blank=True) # image icon if uploaded
    icon_link               = models.URLField(max_length = 512, blank = True, verify_exists = False, null = True) # image icon if on another server, ie Twitter User Photo
    type                    = models.CharField(max_length = 32, blank = True, null = True)
    source_link             = models.CharField(max_length = 512, blank = True,  null = True) #could be absolute URL or path.
    source                  = models.CharField(max_length = 256, blank = True, null = True) #string describing the source
    original_source         = models.CharField(max_length = 256, blank = True, null = True) #if the source pulls content from elsewhere -- see Storify
    original_source_link    = models.URLField(max_length = 512, blank = True, verify_exists = False, null = True)
    offset                  = models.IntegerField(null = True, blank = True) # position within video in seconds.
    private                 = models.BooleanField(default = False) 
    original_data           = models.TextField(blank = True, null = True) #would like to store the original HTML or JSON block here.
    
    
'''

'''
  user.id
  user.name
  user.screen_name
  user.location
  user.description
  user.profile_image_url
  user.profile_background_tile
  user.profile_background_image_url
  user.profile_sidebar_fill_color
  user.profile_background_color
  user.profile_link_color
  user.profile_text_color
  user.protected
  user.utc_offset
  user.time_zone
  user.url
  user.status
  user.statuses_count
  user.followers_count
  user.friends_count
  user.favourites_count
'''
