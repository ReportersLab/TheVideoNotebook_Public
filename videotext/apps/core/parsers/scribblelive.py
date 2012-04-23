from BeautifulSoup import BeautifulSoup
import re, urllib2, argparse
from datetime import datetime, timedelta
from core.models import Note, Video

def parse_scribbling(url, video, import_source = None):
    #we assume that the url passed is of the first page
    #ie: http://livewire.4029tv.com/Event/Republican_Presidential_Debate_September_22_20112?Page=0
    response = urllib2.urlopen(url)
    html = response.read()
    
    soup = BeautifulSoup(html)
    
    
    
    current_nav = soup.find('ul', 'Pagination').findAll('a', 'Current')
    newest = current_nav[-1]
    if newest.text.find('Newest') != -1:
        print 'done'
        return
    
    comments = soup.find('ul', id = 'Posts')
    
    
    for comment in comments.findAll('li'):
        message_text = user_name = link = server_time = icon_link = None
        
        if comment.has_key('style'):
            icon_link = re.search('image:url\((.*)\)', comment['style']).group(1)
        
        if comment.find('div', 'Content') != None:
            message_text = comment.find('div', 'Content').text
        
        if comment.find('em') != None:
            user_name = comment.find('em').text
        
        if comment.find('span', 'Source') and comment.find('span', 'Source').find('a'):
            link = comment.find('span', 'Source').find('a')['href']
        
        #whatever their server time is, not the same as the post time -- offest by 4 hours
        #can't trust it. But we have no choice. This may break during daylight savings...
        full_date = datetime.now()
        if comment.find('span', 'ServerTime') != None:
            server_time = comment.find('span', 'ServerTime').text
            #format: 9/23/2011 1:01:13 AM
            full_date = datetime.strptime(server_time, '%m/%d/%Y %I:%M:%S %p')
            full_date = full_date - timedelta(hours = 4)
        
        
        user = video.user
        if import_source is not None:
            user = import_source.user
        
        
        #since this is rendered in JS, can't get at it. Argh.
        #if comment.find('span', 'Posted') != None:
        #    message_time = comment.find('span', 'Posted').text #there's a script tag in here, hopefully doesn't get pulled in.
        note, created = Note.objects.get_or_create(text = message_text, user_name = user_name, link = link, import_source = import_source, user = user,
                               icon_link = icon_link, video = video, time = full_date, source_link = url, source = 'ScribbleLive')
        #print note
        #print created
        
    
    #Go to the next page
    page_number = re.search('\?Page=(\d+)', url).group(1)
    page_number = '?Page={0}'.format((int(page_number) + 1))
    new_url = re.sub('\?Page=(\d+)', page_number, url)
    
    parse_scribbling(new_url, video, import_source)
    
    
    
    












if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Parses a standard ScribbleLive twitter feed')
    parser.add_argument('url', nargs = '?',  help='the url to scrape' )
    parser.add_argument('video', nargs = '?', type = int, help='the video to add notes to')
    args = parser.parse_args()
    
    v = Video.objects.get(id = args.video)
    
    parse_scribbling(args.url, v)