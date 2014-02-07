#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import expanduser
import urllib, urllib2, time, re, unicodedata, os, sys, locale

class tts():
    """
    @description: Let google2ubuntu to use the Google tts API
    
    @param: the text to read to the user
    """
    def __init__(self,text):
        # need to put this line 
        locale.setlocale(locale.LC_ALL, '')

        # make the program able to switch language
        p = os.path.dirname(os.path.abspath(__file__)).strip('librairy')   
        if os.path.exists(expanduser('~')+'/.config/google2ubuntu/locale.conf'):
            f=open(expanduser('~')+'/.config/google2ubuntu/locale.conf',"r")
            lc = f.readline().strip('\n')
            f.close()
            if lc is not None and lc is not '':
                lang = lc+'_'+lc.upper()
            else:
                lang = locale.getlocale()[0]
                if os.path.isdir(p+'i18n/'+ lang.split('_')[0]) == False:
                    lang='en_EN'
        else:      
            lang = locale.getlocale()[0]
            if os.path.isdir(p+'i18n/'+ lang.split('_')[0]) == False:
                lang='en_EN'

        lc = lang.split('_')[0]
        print lc
        text = unicodedata.normalize('NFKD', unicode(text,"utf-8")).encode('ASCII', 'ignore')
        #text=text.encode("utf8")
        text = text.replace('\n',' ')
        text_list = re.split('(\,|\.)', text)
        combined_text = []
        output=open('/tmp/tts.mp3',"w")
        
        for idx, val in enumerate(text_list):
            if idx % 2 == 0:
                combined_text.append(val)
            else:
                joined_text = ''.join((combined_text.pop(),val))
                if len(joined_text) < 100:
                    combined_text.append(joined_text)
                else:
                    subparts = re.split('( )', joined_text)
                    temp_string = ""
                    temp_array = []
                    for part in subparts:
                        temp_string = temp_string + part
                        if len(temp_string) > 80:
                            temp_array.append(temp_string)
                            temp_string = ""
                    #append final part
                    temp_array.append(temp_string)
                    combined_text.extend(temp_array)
        #download chunks and write them to the output file
        for idx, val in enumerate(combined_text):
            mp3url = "http://translate.google.com/translate_tts?ie=UTF-8&tl=%s&q=%s&total=%s&idx=%s" % (lc, urllib.quote(val), len(combined_text), idx)
            headers = {"Host":"translate.google.com",
            "Referer":"http://www.gstatic.com/translate/sound_player2.swf",
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.163 Safari/535.19"}
            req = urllib2.Request(mp3url, '', headers)
            sys.stdout.write('.')
            sys.stdout.flush()
            if len(val) > 0:
                try:
                    response = urllib2.urlopen(req)
                    output.write(response.read())
                    time.sleep(.5)
                except urllib2.HTTPError as e:
                    print ('%s' % e)
        output.close()


        os.system("play /tmp/tts.mp3 &")
