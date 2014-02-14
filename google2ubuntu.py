#!/usr/bin/env python
# -*- coding: utf-8 -*-
from subprocess import *
from os.path import expanduser
import sys, subprocess, os, json, urllib2, unicodedata, time, gettext, locale

sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/librairy')
from interface import interface
from localehelper import LocaleHelper

localeHelper = LocaleHelper()
lang = localeHelper.getLocale()

t=gettext.translation('google2ubuntu',os.path.dirname(os.path.abspath(__file__))+'/i18n/',languages=[lang])
t.install()


# pause media player if necessary
config = expanduser('~')+'/.config/google2ubuntu/google2ubuntu.conf'
paused = False
try:
    with open(config,"r") as f:
        for line in f.readlines():
            line = line.strip('\n')
            field = line.split('=')
            if field[0] == 'pause' and field[1].replace('"','') != '':
                os.system(field[1].replace('"','')+' &')
                paused = True
            elif field[0] == 'play':
                play_command = field[1].replace('"','')
except Exception:
    print 'Error reading google2ubuntu.conf file'

# launch the recognition                    
g2u = interface()

# restore media player state
print paused
if paused:
    os.system(play_command+' &')
