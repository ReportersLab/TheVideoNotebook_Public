import re, urllib2, argparse
import simplejson as json
from datetime import datetime, timedelta
from videotext.apps.core.models import Note, Video

def parse_storify(url, video):
    json_url = '{0}.json'.format(url)
    read_data = urllib2.urlopen(json_url).read()
    data = json.loads(read_data)
    
    elements = data['elements']
    for e in elements:
        element = elements[e]
        time = datetime.fromtimestamp(float(element['created_at']))
        user_name = user_link = icon_link = None
        
        if element.has_key('author'):
            author = element['author']
            user_name = author.get('name', None)
            #href doesn't work for some reason, even though this is the JSON:
            #"href" : "http://twitter.com/DoyleMcManus",
            user_link = author.get('href', None)
            icon_link = author.get('avatar', None)
        
        message_text = element.get('description', None)
        message_link = element.get('permalink', None)
        source_link = element.get('source', None)
        source = url
        
        note, created = Note.objects.get_or_create(text = message_text, user_name = user_name, link = message_link,
                               icon_link = icon_link, video = video, time = time, source_link = source_link, source = source)
        print note
        print created
    







if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Parses a standard Storify story')
    parser.add_argument('url', nargs = '?',  help='the url of the story (no .json needed)' )
    parser.add_argument('video', nargs = '?', type = int, help='the video to add notes to')
    args = parser.parse_args()
    
    v = Video.objects.get(id = args.video)
    
    parse_storify(args.url, v)