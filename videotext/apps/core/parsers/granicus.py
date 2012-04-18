import re, urllib2, argparse
import simplejson as json
from core.models import Note, Video, Source
from django.conf import settings

'''
pasted url: http://granicus.sandiego.gov/MediaPlayer.php?view_id=3&clip_id=5259
needed url: http://granicus.sandiego.gov/JSON.php?view_id=3&clip_id=5259

format: [ [  { time: "0", type: "text", text: "&gt;&gt; good morning, sh." },
 { time: "0", type: "text", text: "If you can have a seat, we\'re" },
 { time: "3.124", type: "text", text: "going to get started today." },
 { time: "9", type: "meta", text: "Agenda:233659", guid: "4c530d05-10cc-4f20-96f4-998fb65ec44f", title: "&lt;B&gt;&lt;U&gt;ROLL CALL&lt;/B&gt;&lt;/U&gt;" }
 ] ]

'''

def get_granicus_data(source):
    
    json_url = source.url.replace('MediaPlayer.php', 'JSON.php')
    read_data = urllib2.urlopen(json_url).read().decode('utf-8','ignore')
    #ummm. Invalid JSON? keys aren't quoted. Hrm.
    #this is a string, right?
    read_data = read_data.replace('time:', '"time":')
    read_data = read_data.replace('type:', '"type":')
    read_data = read_data.replace('text:', '"text":')
    read_data = read_data.replace('guid:', '"guid":')
    read_data = read_data.replace('title:', '"title":')
    #illegal escapes?
    read_data = read_data.replace("\\'", "'")
    
    data = json.loads(read_data)
    
    try:
        elements = data[0]
        for e in elements:
            time =  float(e['time'])
            text =  e['text']
            type =  e['type']
            
            if type == 'text':
                type = 'caption'
            if type == 'meta':
                text = e['title']
            
            note, created = Note.objects.get_or_create(text = text,
                                                   type = type,
                                                   user = source.user,
                                                   user_name = source.user.username,
                                                   video = source.video,
                                                   source_link = source.url,
                                                   source = 'Granicus',
                                                   original_source = 'Granicus',
                                                   offset = time,
                                                   original_source_link = json_url,
                                                   private = False,
                                                   original_data = e,
                                                   import_source = source)
            
    except:
        print 'error'

