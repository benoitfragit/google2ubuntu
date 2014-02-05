#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, gettext, locale, os

sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/librairy')

from interface import interface

lang = locale.getlocale()[0]
if os.path.isdir(os.path.dirname(os.path.abspath(__file__))+'/i18n/'+lang.split('_')[0]) == False:
    lang='en_EN'

gettext.install('google2ubuntu',os.path.dirname(os.path.abspath(__file__))+'/i18n/')

g2u = interface()
