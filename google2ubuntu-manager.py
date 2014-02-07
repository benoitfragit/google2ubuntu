#!/usr/bin/env python
# -*- coding: utf-8 -*-  
from gi.repository import Gtk
from gi.repository import Notify
from gi.repository import Gdk
from gi.repository import Gio
from os.path import expanduser
import os
import sys
import subprocess
import gettext
import locale
import xml.etree.ElementTree as ET

sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/librairy')
from MainWindow import *

if os.path.exists(expanduser('~')+'/.config/google2ubuntu/locale.conf'):
    f=open(expanduser('~')+'/.config/google2ubuntu/locale.conf',"r")
    lc = f.readline().strip('\n')
    f.close()
    if lc is not None and lc is not '':
        lang = lc
    else:
        lang = (locale.getlocale()[0]).split('_')[0]
        if os.path.isdir(os.path.dirname(os.path.abspath(__file__))+'/i18n/'+lang) == False:
            lang='en'        
else:      
    lc = locale.getlocale()[0]
    lang = lc.split('_')[0]
    if os.path.isdir(os.path.dirname(os.path.abspath(__file__))+'/i18n/'+lang) == False:
        lang='en'

t=gettext.translation('google2ubuntu',os.path.dirname(os.path.abspath(__file__))+'/i18n/',languages=[lang])
t.install()

#keep the old way for the moment
#gettext.install('google2ubuntu',os.path.dirname(os.path.abspath(__file__))+'/i18n/')

# application principale
class MyApplication(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        win = MainWindow(self)
        win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)
            

app = MyApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)
