import csv, urllib2, StringIO
from django.http import HttpResponse
from django.conf import settings
from core.models import Note, Video
from datetime import datetime

def import_tvn_csv(source):
    
    data = source.csv_data.decode('utf-8')
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
        note, created = Note.objects.get_or_create(
                                   text = row['text'].decode('utf8'),
                                   time =  datetime.strptime(row['time'], '%Y-%m-%dT%H:%M:%S.000Z') if row['time'] else None,
                                   user_name = row['user_name'],
                                   user = row.get('user', None),
                                   video = video,
                                   link = row['link'],
                                   icon = row['icon'],
                                   icon_link = row['icon_link'],
                                   type = row['type'],
                                   source_link = row['source_link'],
                                   source = row['source'],
                                   offset = row['offset'],
                                   private = row['private']
        )
        

def export_tvn_csv(video):
    response = HttpResponse(mimetype = 'text/csv')
    response['Content-Disposition'] = 'attachment; filename=notes.csv'
    writer = csv.writer(response)
    
    writer.writerow([
        'text', 'time', 'user_id', 'user_name', 'user_link', 'video_id', 'link', 'icon', 'icon_link', 'type', 'source_link', 'source', 'offset', 'private',
        'creation_time', 'update_time',
    ])
    
    for note in video.note_set.all():
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
    
    
    
