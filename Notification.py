#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Notify
import time

# Cette classe utilis Notify pour alerter l'utilisateur
class notification():
    # initialisation du serveur de notification
    def __init__(self,titre,corps):
        Notify.init(titre)
        self.n = Notify.Notification.new(titre,corps,"")
        self.n.set_urgency(Notify.Urgency.CRITICAL)    
        self.n.set_icon_from_pixbuf(Gtk.Label().render_icon(Gtk.STOCK_MEDIA_PLAY, Gtk.IconSize.DIALOG))
        self.n.show()
        time.sleep(0.5)

    # on mets à jours la notification
    def update(self,titre,text,typeicon):
        self.n.update(titre,text,"")
        if typeicon == 'RECORD':
            self.n.set_icon_from_pixbuf(Gtk.Label().render_icon(Gtk.STOCK_MEDIA_RECORD, Gtk.IconSize.DIALOG))
        elif typeicon == 'NETWORK':
            self.n.set_icon_from_pixbuf(Gtk.Label().render_icon(Gtk.STOCK_MEDIA_RECORD, Gtk.IconSize.DIALOG))
        elif typeicon == 'EXECUTE':
            self.n.set_icon_from_pixbuf(Gtk.Label().render_icon(Gtk.STOCK_EXECUTE, Gtk.IconSize.DIALOG))
        elif typeicon == 'ERROR':
            self.n.set_icon_from_pixbuf(Gtk.Label().render_icon(Gtk.STOCK_DIALOG_ERROR, Gtk.IconSize.DIALOG))   
        else:
            self.n.set_icon_from_pixbuf(Gtk.Label().render_icon(Gtk.STOCK_INFO, Gtk.IconSize.DIALOG))    
        
        self.n.show()
    
    # on quitte
    def close(self):
        self.n.close()
