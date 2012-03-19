from BeautifulSoup import BeautifulSoup
import re, urllib2, argparse
from datetime import datetime, timedelta
from core.models import Note, Video

def parse_fark(url, video, import_source = None):
    
    #http://www.fark.com/comments/6585847/Bachmann-Perry-Romney-those-other-people-who-think-they-have-a-chance-at-GOP-presidential-nomination-square-off-in-second-GOP-2012-Debate-Watch-derp-fly-discuss-it-here?cpp=1
    headers = { 'User-Agent': 'Mozilla/5.0'}
    request = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(request)
    html = response.read()
    soup = BeautifulSoup(html)
    
    source = "Fark.com"
    comments = soup.find('div', id = 'commentsArea')
    
    for table in comments.findAll('table'):
        
        user_name = table.find('td', 'clogin').find('a').text
        user_link = table.find('td', 'clogin').find('a')['href']
        message_link = table.find('td', 'cdate').find('a')['href']
        date = table.find('td', 'cdate').find('a').text
        time = datetime.strptime(date, '%Y-%m-%d %I:%M:%S %p')
        
        #have to get the next sibling to this table. But nextSibling doesn't work
        #look back in the main comments soup and extract from there.
        text_id = table['id'].replace('ctable', 'ct')
        text = comments.find('div', id = text_id).text
        
        user = video.user
        if import_source is not None:
            user = import_source.user
        
        
        
        note, created = Note.objects.get_or_create(text = text, user_name = user_name, user_link = user_link, link = message_link,
                               video = video, time = time, source_link = url, source = source, import_source = import_source, user = user)
        print note
        print created
    







if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Parses a standard Fark comment thread')
    parser.add_argument('url', nargs = '?',  help='the url of the thread. If you want all pages, be sure to use the single page option' )
    parser.add_argument('video', nargs = '?', type = int, help='the video to add notes to')
    args = parser.parse_args()
    
    v = Video.objects.get(id = args.video)
    
    parse_fark(args.url, v)