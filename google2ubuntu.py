#!/usr/bin/env python
# -*- coding: utf-8 -*-
from subprocess import *
from os.path import expanduser
import sys, subprocess, os, json, urllib2, unicodedata, time, gettext, locale

sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/librairy')
from interface import interface

if os.path.exists(expanduser('~')+'/.config/google2ubuntu/locale.conf'):
    f=open(expanduser('~')+'/.config/google2ubuntu/locale.conf',"r")
    lc = f.readline().strip('\n')
    f.close()
    if lc is not None and lc is not '':
        lang = lc
    else:
        # better to check getlocale to retrieve default locale
        lang = (locale.getlocale()[0]).split('_')[0]
        # if default locale not supported take en as default
        if os.path.isdir(os.path.dirname(os.path.abspath(__file__))+'/i18n/'+lang) == False:
            lang = 'en'
else:      
    lc = locale.getlocale()[0]
    lang = lc.split('_')[0]
    if os.path.isdir(os.path.dirname(os.path.abspath(__file__))+'/i18n/'+lang) == False:
        lang='en'

t=gettext.translation('google2ubuntu',os.path.dirname(os.path.abspath(__file__))+'/i18n/',languages=[lang])
t.install()

#keep the old way for the moment
#gettext.install('google2ubuntu',os.path.dirname(os.path.abspath(__file__))+'/i18n/')
g2u = interface()
