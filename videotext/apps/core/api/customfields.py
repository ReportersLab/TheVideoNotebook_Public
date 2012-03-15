import dateutil
import pytz
import re
from tastypie import fields
from tastypie.exceptions import ApiFieldError

from django.conf import settings
from django.utils import datetime_safe

DATETIME_REGEX = re.compile('^(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})(T|\s+)(?P<hour>\d{2}):(?P<minute>\d{2}):(?P<second>\d{2}).*?$')


def string_to_local_datetime(value):
    #generate a date
    parsed = dateutil.parser.parse(value)
    try:
        #create a pytz timezone instance at the Django server time
        django_tz = pytz.timezone(settings.TIME_ZONE)
        #return the date in django time. From the client it should always come in as UTC time
        return parsed.astimezone(django_tz)
    except ValueError: # datetime without timezone information
        return parsed

'''
Partially from here: https://github.com/toastdriven/django-tastypie/issues/118

I was running into a problem where if you were out of the timezone the server was in, syncing video times would be incorrect.
This was happening because...

1) The client was sending UTC dates. So, if you were in Eastern Time it'd add 5 hours. Pacific time would add 8.
2) TastyPie was trying to help (I believe it was TastyPie) by converting from UTC into server time.
   BUT, the assumption it was making was that the client was sending UTC converted from server time. This led to times all being
   off by whatever the client timezone was from the server timezone (so, pacific notes would be 3 hours earlier than the video)

The below class is an attempt to fix that. Essentially before sending any information it converts it to UTC time so the time displayed by the
client is in local time (JS just takes the UTC date and makes it a local date). On the way in the UTC time is converted into server time correctly.

This seems to work.
'''
class TzDateTimeField(fields.DateTimeField):
    
    #this is much the same as the default implementation, but adds TZ info.
    #Note that this is for Django 1.3. If TVN gets updated to Djangon 1.4, I believe everything is built in.
    def convert(self, value):
        if value is None:
            return None
        if isinstance(value, basestring):
            match = DATETIME_REGEX.search(value)

            if match:
                data = match.groupdict()
                d = datetime_safe.datetime(int(data['year']), int(data['month']), int(data['day']), int(data['hour']), int(data['minute']), int(data['second']), tzinfo = pytz.timezone(settings.TIME_ZONE) )
                return d.astimezone(pytz.utc)
            else:
                raise ApiFieldError("Datetime provided to '%s' field doesn't appear to be a valid datetime string: '%s'" % (self.instance_name, value))
        
        #first create a pytz timezone of whatever the Django Timezone is in the settings.
        django_tz = pytz.timezone(settings.TIME_ZONE)
        #If there is no timezone for the data (when the data is coming in, it IS TZ aware)
        if value.tzinfo is None:
            #then convert the naive time to whatever the django time is (this effectively keeps it the same, but is necessary to have that info before
            #going to UTC time)
            value = django_tz.localize(value)
        #now send the data back as UTC
        return value.astimezone(pytz.utc)
    
    """
    A datetime field that honors timezone information.
    """
    def hydrate(self, bundle):
        value = fields.ApiField.hydrate(self, bundle)
        
        if value and not hasattr(value, 'year'):
            try:
                # Try to rip a date/datetime out of it.
                value = string_to_local_datetime(value)
            except ValueError:
                pass
        return value