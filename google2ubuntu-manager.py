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
import xml.etree.ElementTree as ET

sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/librairy')
from MainWindow import *
from localehelper import LocaleHelper

localeHelper = LocaleHelper()
lang = localeHelper.getLocale()

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
        localeHelper = LocaleHelper()
        lang = localeHelper.getLocale()

        t=gettext.translation('google2ubuntu',os.path.dirname(os.path.abspath(__file__))+'/i18n/',languages=[lang])
        t.install()

    def do_startup(self):
        Gtk.Application.do_startup(self)
            

app = MyApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)
