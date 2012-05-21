import re, urllib2, argparse
import simplejson as json
import dateutil
from core.models import Note, Video
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import datetime_safe
import pytz


API_BASE = 'http://api.storify.com/v1/stories/'
DATETIME_REGEX = re.compile('^(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})(T|\s+)(?P<hour>\d{2}):(?P<minute>\d{2}):(?P<second>\d{2}).*?$')


def parse_storify(url, video, import_source):
    url_pieces = url.split('/')
    name = url_pieces[-2]
    slug = url_pieces[-1]
    json_url = '{0}{1}/{2}?per_page=1000'.format(API_BASE, name, slug)
    #print '========================='
    read_data = urllib2.urlopen(json_url).read()
    data = json.loads(read_data)
    #print data
    elements = data['content']['elements']
    permalink = data['content']['permalink']
    for e in elements:
        element = e
        time = convert_time(element['posted_at'])
        type = element['type']
        
        #there are other types, but we'd have to write a better parser and UI for them. Let's keep only the quotes.
        #print type
        
        if type != "quote":
            continue
        
        text = element['data'][type]['text']
        #print text
        source_link = '{0}/elements/{1}'.format(permalink, element['id'])
        source = 'Storify'
        user_name = user_link = icon_link = original_source = original_source_link = None
        
        if element.has_key('source'):
            original_source = element['source']['name']
            original_source_link = element['source']['href']
            
        if element.has_key('attribution'):
            author = element['attribution']
            user_name = author.get('username', None)
            user_link = author.get('href', None)
            icon_link = author.get('thumbnail', None)
        
        
        
        note, created = Note.objects.get_or_create(text = text,
                                                   type = type,
                                                   user = import_source.user,
                                                   user_name = user_name,
                                                   user_link = user_link,
                                                   icon_link = icon_link,
                                                   video = video,
                                                   time = time,
                                                   source_link = source_link,
                                                   source = source,
                                                   original_source = original_source,
                                                   original_source_link = original_source_link,
                                                   private = False,
                                                   original_data = element,
                                                   import_source = import_source,
                                                   import_source_name = import_source.name)
        #print note
        

def convert_time(value):
        if value is None:
            return None
        if isinstance(value, basestring):
            match = DATETIME_REGEX.search(value)

            if match:
                data = match.groupdict()
                d = datetime_safe.datetime(int(data['year']), int(data['month']), int(data['day']), int(data['hour']), int(data['minute']), int(data['second']), tzinfo = pytz.timezone(settings.TIME_ZONE) )
                return d.astimezone(pytz.utc)
            else:
                return #should raise an error 
        #first create a pytz timezone of whatever the Django Timezone is in the settings.
        django_tz = pytz.timezone(settings.TIME_ZONE)
        #If there is no timezone for the data (when the data is coming in, it IS TZ aware)
        if value.tzinfo is None:
            #then convert the naive time to whatever the django time is (this effectively keeps it the same, but is necessary to have that info before
            #going to UTC time)
            value = django_tz.localize(value)
        #now send the data back as UTC
        return value.astimezone(pytz.utc)



if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Parses a standard Storify story')
    parser.add_argument('url', nargs = '?',  help='the url of the story (no .json needed)' )
    parser.add_argument('video', nargs = '?', type = int, help='the video to add notes to')
    args = parser.parse_args()
    
    v = Video.objects.get(id = args.video)
    
    parse_storify(args.url, v)