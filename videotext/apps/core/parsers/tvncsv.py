import csv, urllib2, StringIO
from django.http import HttpResponse
from django.conf import settings
from django.utils.encoding import smart_str, smart_unicode
from core.models import Note, Video
from datetime import datetime

def import_tvn_csv(source):
    
    data = smart_str(source.csv_data)
    if not source.csv_data or source.csv_data == '':
        url = source.url
        if source.content is not None and source.content != '':
            url = 'http://{0}/{1}'.format(settings.AWS_STORAGE_BUCKET_NAME, source.content)
        data = urllib2.urlopen( url )
    else:
        data = StringIO.StringIO(data)
    
    reader = csv.DictReader(data)
    video = source.video
    if not video:
        return
    for row in reader:
        
        time = None
        
        try:
            if row['time']:
                time =  datetime.strptime(row['time'], '%Y-%m-%dT%H:%M:%S.000Z')
        except:
            pass
        
        note, created = Note.objects.get_or_create(
                                   text = row.get('text', ''),
                                   time = time,
                                   user_name = source.user.username, #Let's not allow importers to just assign notes to users.
                                   user = source.user, #let's not allow importers to just assign notes to other users.
                                   video = video,
                                   icon = row.get('icon', ''),
                                   icon_link = row.get('icon_link', ''),
                                   type = row.get('type', 'note'),
                                   source_link = row.get('source_link', ''),
                                   source = row.get('source', 'CSV'),
                                   offset = int(row.get('offset', 0)),
                                   private = row.get('private', False),
                                   import_source = source,
                                   import_source_name = source.name
        )
        

def export_tvn_csv(notes):
    response = HttpResponse(mimetype = 'text/csv')
    response['Content-Disposition'] = 'attachment; filename=notes.csv'
    writer = csv.writer(response)
    
    writer.writerow([
        'text', 'time', 'user_id', 'user_name', 'user_link', 'video_id', 'link', 'icon', 'icon_link', 'type', 'source_link', 'source', 'offset', 'private',
        'creation_time', 'update_time',
    ])
    
    
    
    for note in notes:
        writer.writerow([
            note.text.encode('utf8'),
            note.time.strftime('%Y-%m-%dT%H:%M:%S.000Z') if note.time else '',
            note.user.id if note.user else '',
            note.user_name,
            note.user_link,
            note.video.id if note.video else '',
            note.link,
            note.icon,
            note.icon_link,
            note.type,
            note.source_link,
            note.source,
            note.offset,
            note.private,
            note.creation_time.strftime('%Y-%m-%dT%H:%M:%S.000Z') if note.creation_time else '',
            note.update_time.strftime('%Y-%m-%dT%H:%M:%S.000Z') if note.update_time else '',
        ])
    
    return response
    
    
    
