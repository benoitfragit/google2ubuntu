#!/usr/bin/env python
# -*- coding: utf-8 -*-
from subprocess import *
from os.path import expanduser
from librairy import LocaleHelper
import sys, subprocess, os, json, urllib2, unicodedata, time, gettext, locale

sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/librairy')
from interface import interface

localeHelper = LocaleHelper()
lang = localeHelper.getLocale()

t=gettext.translation('google2ubuntu',os.path.dirname(os.path.abspath(__file__))+'/i18n/',languages=[lang])
t.install()

#keep the old way for the moment
#gettext.install('google2ubuntu',os.path.dirname(os.path.abspath(__file__))+'/i18n/')
g2u = interface()
