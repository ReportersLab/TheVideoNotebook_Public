from pysrt import SubRipFile
from core.models import Note, Video, Source





def get_srt_data(source):
    captions = SubRipFile.from_string(source.srt_data)
    for c in captions:
        start = c.start.to_time()
        end = c.end.to_time()
        offset = start.second + (start.minute * 60) + (start.hour * 60 * 60) + (start.microsecond / 1000000) #it can't possibly be more than hours.
        end_offset = end.second + (end.minute * 60) + (end.hour * 60 * 60) + (end.microsecond / 1000000)
        
        
        note, created = Note.objects.get_or_create(
            text = c.text,
            offset = end_offset,
            #end_offset = end_offset,
            user = source.user,
            user_name = source.user.username,
            video = source.video,
            private = False,
            import_source = source,
            source = 'SRT File',
            original_source = 'SRT File',
            source_link = source.url, #they're probably not going to have one of these...
            type = "caption"
        )
        
        
