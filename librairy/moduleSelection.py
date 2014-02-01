#!/usr/bin/env python
# -*- coding: utf-8 -*-  
from gi.repository import Gtk
from gi.repository import Notify
from gi.repository import Gdk
from gi.repository import Gio
from os.path import expanduser
import os, sys, subprocess, gettext

gettext.install('google2ubuntu',os.path.dirname(os.path.abspath(__file__))+'/i18n/')

# gère l'apparition de la fenêtre de choix du module
class moduleSelection():
    def __init__(self):
        w=Gtk.Window()
        dialog = Gtk.FileChooserDialog(_("Choose a file"), w,Gtk.FileChooserAction.OPEN,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,Gtk.STOCK_OPEN, Gtk.ResponseType.OK))        
        dialog.set_default_size(800, 400)

        response = dialog.run()
        self.module = '-1'
        if response == Gtk.ResponseType.OK:
            self.module=dialog.get_filename()
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()
    
    def getModule(self):
        return self.module
