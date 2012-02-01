from windmill.authoring import WindmillTestClient
from BeautifulSoup import BeautifulSoup
from datetime import datetime
import re, urlparse
from copy import copy
from core.models import Note, Video
import functest




def test_scrape_coveritlive():
    
    client = WindmillTestClient(__name__)
    #client.open(url = 'http://www.coveritlive.com/index2.php/option=com_altcaster/task=viewaltcast/altcast_code=c3c11df0e3/height=600/width=608')
    client.waits.sleep(milliseconds=2000)
    #client.click(id="divsrc2")
    client.execJS(js='displayAuthModal(true)') # removes the "play" button, activates chat.
    #client.waits.sleep(milliseconds=5000) # just wait a couple of seconds for this to load. May want to change to waits.forElement
    client.waits.forElement(classname=u"chatmsg", timeout=10000)
    
    #if there are additional entries, they'll be hidden and AJAX will be required. Let's click the buttons
    #literally no variations of this click work for me.
    #client.click(jquery=u'("td.addlentrytext a")')
    #client.click(xpath=u"//td[@class='addlentrytext']/a")
    
    
    #not totally sure how to wait only until all ajax calls are done, since the ids are random.
    #client.waits.sleep(milliseconds=5000)
    
    #gets the current HTML, after JS has loaded.
    
    trigger_additional_entries(client)
    
    
    
    
    # Create soup from the full page and get desired information
    response = client.commands.getPageText()
    assert response['status']
    assert response['result']
    
    soup = BeautifulSoup(response['result'])
    
    
    
    #container for messages / dates
    message_container = soup.find('div', id = 'mainchattext')
    
    #messages = soup.findAll("div", "chatmsg")
           
    dateline = None
    '''
    this will find all subdivs, in some cases the chatmsg is within another subdiv. This happens if
    there are too many entries in the liveblog and it makes you load the extras via ajax.
    '''
    messages = []
    for message in message_container.findAll('div'):
        if message.has_key('id') and message['id'].find('entry') != -1:
            for m in message.findAll('div'):
                messages.append(m)
        else:
            messages.append(message)
    
    
    for message in messages:
        if not message.has_key('class'):
            print message
            continue
        #try:
        if message['class'].find('dateline') != -1:
            #format: Day-Of-Week Month Date, Year
            #format: %A %B %d, %Y
            dateline = message.text
            print dateline
        
        if message['class'].find('chatmsg') != -1:
            parse_chat_message(message, dateline)
        
        
        #except:
        #    print message    
        
        
        
 
def parse_chat_message(message, dateline):
    #last message is a cover-it-live ad.
    if message['class'].find('eventcompletedimage') != -1:
        return
    
    #format: h:mm
    #format: %I:%M
    message_time = message.find("div", "itemtime").text
    
    #avatars and message text are kept in spans, no easy way to tell the difference unless
    #beautiful soup has a "does not contain classname" function I don't know about.
    message_text = message.find('span', {'id': True}).text
    
    message_image = None
    user_link = None
    user_name = None
    if message.find('span', 'writeravatar') != None and message.find('span', 'writeravatar').find('img') != None:
        message_image = message.find('span', 'writeravatar').find('img')['src']
    if message.find('span', 'tweetavatar'):
        message_image = message.find('span', 'tweetavatar').find('img')['src']
        user_link = message.find('span', 'tweetavatar').find('a')['href']
        
    
    if message.find('div', 'inlinedisplayname') != None:
        user_name = message.find('div', 'inlinedisplayname').text #may not exist
        user_name = user_name.replace(':&nbsp;', '')
    if message.find('span', 'commentfrom') != None:
        user_name = message.find('span', 'commentfrom').text
        user_name = user_name.replace('Comment From ', '')
    
    #create date stamp
    #blasted Cover-It-Live doesn't include AM/PM anywhere. Not even sure how to begin to deal with that.
    #I suppose you could pass in the AM/PMness of the first comment and calculate from there...?
    full_date = datetime.now()
    am_pm = functest.registry.get('am_pm', 'PM')
    if dateline != None:
        #TODO: something has to be done to calculate whether we've changed am/pm here.
        full_time = "{0} {1} {2}".format(dateline, message_time, am_pm)
        full_date = datetime.strptime(full_time, '%A %B %d, %Y %I:%M %p')
    
    video = None
    if functest.registry.has_key('video'):
        video = Video.objects.get(id = functest.registry['video'])
    
    source_link = functest.registry.get('source', '')
    
    note, created = Note.objects.get_or_create(text = message_text, user_name = user_name, user_link = user_link,
                               icon_link = message_image, video = video, time = full_date, source = 'Cover-It-Live', source_link = source_link)
    
    print note
    print created
    '''
    print full_date
    print user_name
    print user_link
    print message_text
    print message_image
    #passed through command line
    print functest.registry['video']
    '''
    
    

def trigger_additional_entries(client):
    #since I cannot get the client to click properly, I'm going to trigger this via the JS
    #located in the <a> tags. Yech.
    response = client.commands.getPageText()
    assert response['status']
    assert response['result']
    
    soup = BeautifulSoup(response['result'])
    
    
    for cell in soup.findAll('td', 'addlentryicon'):
        #get anchor tag
        a = cell.find('a')
        
        if a == None:
            print "no anchor"
            return
        
        if a.has_key('onclick'):
            #script that the anchor fires to expand element
            script = a['onclick']
            #I am not capable of writing this in a way that works. I just want the digits...
            ajax_target_search = re.search("(ajax)\d+", script)
            ajax_target = 'entry{0}'.format(ajax_target_search.group(0).replace('ajax',''))
            
            script = script.replace('return false;', '')
            client.execJS(js=script)
            client.waits.forElement(id=ajax_target)
        else:
            print a