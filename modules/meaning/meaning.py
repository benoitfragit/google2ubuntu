#!/usr/bin/env python
# -*- coding: utf-8 -*-
from subprocess import *
from os.path import expanduser
import sys, subprocess, os, json, unicodedata, time, locale
from urllib2 import urlopen

locale.setlocale(locale.LC_ALL, '')
lang = locale.getdefaultlocale()[0]
lang=lang.split('_')[0]

sys.path.append('/usr/share/google2ubuntu/librairy')
from Googletts import tts

if len(sys.argv) >= 2:
    null = None
    keyword = sys.argv[1]
    #keyword = keyword.replace(' ','+')
    print keyword
    data = urlopen("http://www.google.com/dictionary/json?callback=dict_api.callbacks.id100&q="+keyword+"&sl="+lang+"&tl="+lang+"&restrict=pr%2Cde&client=te").read()[25:-1]
 
    d = eval('('+data+')')
    if d[1] == 200:
        result = d[0]
          
        if 'webDefinitions' in result:
            webd = result.get('webDefinitions')[0]
            entries = webd.get('entries')
            entry=entries[0]
            for term in entry.get('terms'):
                if term.get('type') == 'text':
                    tts(term.get('text'))
