#!/usr/bin/env python
# -*- coding: utf-8 -*-  
from gi.repository import Gtk
from gi.repository import Notify
from gi.repository import Gdk
from gi.repository import Gio
from os.path import expanduser
import os, sys, subprocess, gettext

# gère l'apparition de le fenêtre d'aide
class HelpWindow():
    """
    @description: Diaplay an help window
    """
    def __init__(self):
        #a  Gtk.AboutDialog
        self.aboutdialog = Gtk.AboutDialog()

        # lists of authors and documenters (will be used later)
        authors = ["Franquet Benoit"]
        documenters = ["Franquet Benoit"]
        translators = "Franquet Benoit <benoitfranquet@gmail.com>\n"
        translators += "Tectas\n"
        translators += "Daniele Scasciafratte <mte90net@gmail.com>\n"
        translators += "Leor <leor.bi.otti.flor@gmail.com﻿>\n"
        translators += "Ladios\n"
        translators += "Franck Claessen"

        # we fill in the aboutdialog
        self.aboutdialog.set_program_name(_("Help Google2Ubuntu"))
        self.aboutdialog.set_copyright("Copyright \xc2\xa9 2014 Franquet Benoit")
        self.aboutdialog.set_authors(authors)
        self.aboutdialog.set_translator_credits(translators) 
        self.aboutdialog.set_documenters(documenters)
        self.aboutdialog.set_version("1.1.1")
        self.aboutdialog.set_license_type (Gtk.License.GPL_3_0,)
        self.aboutdialog.set_website("https://github.com/benoitfragit/google2ubuntu")
        self.aboutdialog.set_website_label("https://github.com/benoitfragit/google2ubuntu")

        # we do not want to show the title, which by default would be "About AboutDialog Example"
        # we have to reset the title of the messagedialog window after setting the program name
        self.aboutdialog.set_title("")

        # to close the aboutdialog when "close" is clicked we connect the
        # "response" signal to on_close
        self.aboutdialog.connect("response", self.on_close)
        # show the aboutdialog
        self.aboutdialog.show()
        
    # destroy the aboutdialog
    def on_close(self, action, parameter):
        """
        @description: function called when the user wants to close the window
        
        @param: action
            the window to close
        """
        action.destroy()
