#!/usr/bin/env python
# -*- coding: utf-8 -*-  
from gi.repository import Gtk
from gi.repository import Notify
from gi.repository import Gdk
from gi.repository import Gio
from os.path import expanduser
from add_window import add_window
import os
import sys
import subprocess
import gettext

gettext.install('google2ubuntu',os.path.dirname(os.path.abspath(__file__))+'/i18n/')

# Classe MyWindow gere l'apparition de la fenêtre principale
class MainWindow(Gtk.ApplicationWindow):
    """
    @description: This class display the main window that the user will 
    see when he wants to manage his commands
    """
    def __init__(self,app):
        Gtk.Window.__init__(self, title="google2ubuntu-manager",application=app)
        self.set_default_size(700, 500)  
        self.set_resizable(True)     
        self.set_border_width(0)
        self.get_focus()
        self.set_position(Gtk.WindowPosition.CENTER)
        path = os.path.dirname(os.path.abspath(__file__)).strip('librairy')
        self.set_default_icon_from_file(path+'/resources/icons.png')
        
        content = add_window()
                
        # show
        self.add(content.get_grid())
        self.show_all()
