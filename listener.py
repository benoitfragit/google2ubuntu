# Okay Google hotword activation script
# Josh Chen, 14 Feb 2014
# Feel free to modify as you need

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from subprocess import *
from os.path import expanduser
import sys, subprocess, os, json, urllib2, unicodedata, time, gettext, locale, gettext

p = os.path.dirname(os.path.abspath(__file__))

sys.path.append( p +'/librairy')
from localehelper import LocaleHelper

localeHelper = LocaleHelper()
lang = localeHelper.getLocale()

t=gettext.translation('google2ubuntu',p +'/i18n/',languages=[lang])
t.install()

hotword = _('ok start')
config_file = expanduser('~') + '/.config/google2ubuntu/google2ubuntu.conf'
try:
    if os.path.exists(config_file):
        f=open(config_file,'r')
        for line in f.readlines():
            line = line.strip('\n')
            field = line.split('=')
            if field[0] == 'hotword':  
                hotword = field[1].replace('"','')
        f.close()
except Exception:
    print "Error loading", config_file
    sys.exit(1)


# lecture du fichier audio
filename='/tmp/pingvox.flac'
f = open(filename)
data = f.read()
f.close()

try:
    # Send request to Google
    fail = 'req'
    req = urllib2.Request('https://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&lang='+lang, data=data, headers={'Content-type': 'audio/x-flac; rate=16000'})
    
    fail = 'ret'
    # Return request
    ret = urllib2.urlopen(req)
    
    # Google translate API sometimes returns lists of phrases. We'll join them all up into a single phrase again
    phrase = ''
    t = ret.read().split('\n')
    t.remove('')
    for i in t:
        s = json.loads(i)
        if len(s['hypotheses']) > 0:
            phrase = phrase + s['hypotheses'][0]['utterance'] + ' '
    print "Recognition: "+phrase
        
    fail = 'parse'
    # Parse
    #text=json.loads(d)['hypotheses'][0]['utterance']
    
    print "hotword:", hotword
    print "detected:", phrase   
    if phrase.lower().count(hotword.lower()) > 0: 
        os.system('python ' + p + '/google2ubuntu.py')

except Exception:
    os.system('echo Fail:'+fail) # for debugging
    #message = _('unable to translate')
    if fail == 'req':
        message = _('Cannot connect to Google Translate')
    elif fail == 'parse':
        message = _('Phrase parsing failed')
    elif fail == 'ret':
        message = _('Error processing value returned by Google Translate')
    
    print message
    sys.exit(1)
