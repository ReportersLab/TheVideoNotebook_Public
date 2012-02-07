import csv
from django.http import HttpResponse

def import_tvn_csv():
    pass

def export_tvn_csv(video):
    response = HttpResponse(mimetype = 'text/csv')
    response['Content-Disposition'] = 'attachment; filename=decisionmakers.csv'
    writer = csv.writer(response)
    
    writer.writerow([
        'text', 'time', 'user_id', 'user_name', 'user_link', 'video_id', 'link', 'icon', 'icon_link', 'type', 'source_link', 'source', 'offset', 'private',
        'creation_time', 'update_time',
    ])
    
    for note in video.note_set.all():
        writer.writerow([
            note.text.encode('utf8'), note.time.strftime('%Y-%m-%dT%H:%M:%S.000Z'), note.user.id if note.user else '', note.user_name, note.user_link, note.video.id if note.video else '', note.link, note.icon, note.icon_link, note.type, note.source_link,
            note.source, note.offset, note.private, note.creation_time.strftime('%Y-%m-%dT%H:%M:%S.000Z'), note.update_time.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        ])
    
    return response
    
    
    
