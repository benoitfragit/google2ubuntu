#!/usr/bin/env python
# -*- coding: utf-8 -*-  
from gi.repository import Gtk
from gi.repository import Notify
from gi.repository import Gdk
from gi.repository import Gio
from os.path import expanduser
from localehelper import LocaleHelper
import os, sys, gettext

class SetupWindow():
    def __init__(self,button_back):
        # class variables
        localeHelper = LocaleHelper('en_EN')
        self.locale = localeHelper.getLocale()
        self.recording_time = 5
        self.player_pause = ''
        self.player_play = ''
        self.dictation = False
        self.config = expanduser('~')+'/.config/google2ubuntu/google2ubuntu.conf'
        
        # looking for the configuration file
        self.__loadconfig()

        label1=Gtk.Label(_('Select your language'))
        label1.set_justify(Gtk.Justification.LEFT)
        label1.set_halign(Gtk.Align.START)
        label2=Gtk.Label(_('Set the recording time (seconds)'))
        label2.set_justify(Gtk.Justification.LEFT) 
        label2.set_halign(Gtk.Align.START) 
        label4=Gtk.Label(_("Set the music player's play command"))
        label4.set_justify(Gtk.Justification.LEFT) 
        label4.set_halign(Gtk.Align.START) 
        label5=Gtk.Label(_("Set the music player's pause command"))
        label5.set_justify(Gtk.Justification.LEFT) 
        label5.set_halign(Gtk.Align.START) 
        
        combo = self.__get_combobox()
        
        self.scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL,1,10,1)
        self.scale.set_value(self.recording_time)
        self.scale.connect("value-changed", self.scale_moved)
        self.scale.set_tooltip_text(_('Change the recording time'))
                
        self.entry1 = Gtk.Entry()
        self.entry1.set_text(self.player_play)
        self.entry1.set_tooltip_text(_('Set the play command'))
        
        
        self.entry2 = Gtk.Entry()
        self.entry2.set_text(self.player_pause)
        self.entry2.set_tooltip_text(_('Set the pause command'))

        #button_back = Gtk.Button.new_from_stock(Gtk.STOCK_OK)
        button_back.connect("clicked",self.on_clicked)
        
        # an invisble widget to fill the window
        ll = Gtk.Label()
        ll.set_vexpand(True)
        
        self.grid = Gtk.Grid()
        self.grid.set_border_width(10)
        self.grid.set_row_spacing(15)
        self.grid.set_vexpand(True)
        self.grid.set_column_spacing(5)
        self.grid.set_column_homogeneous(True)
        self.grid.attach(label1,0,0,4,1)
        self.grid.attach(combo,4,0,2,1)
        self.grid.attach(label2,0,1,4,1)
        self.grid.attach(self.scale, 4,1,2,1)
        self.grid.attach(label4,0,2,4,1)
        self.grid.attach(self.entry1,4,2,2,1)
        self.grid.attach(label5,0,3,4,1)
        self.grid.attach(self.entry2,4,3,2,1)
        self.grid.attach(ll,0,4,6,1)
        self.grid.attach(button_back,5,5,1,1)        

    
    # load the config    
    def __loadconfig(self):
        # if a config file is available
        if os.path.exists(self.config):
            try:
                # here we load
                with open(self.config,"r") as f:
                    for line in f.readlines():
                        line = line.strip('\n')
                        #get the field
                        field = line.split('=')
                        if len(field) >= 2:
                            if field[0] == 'recording':
                                self.recording_time=int(field[1])
                            elif field[0] == 'pause':
                                self.player_pause = field[1]
                            elif field[0] == 'play':
                                self.player_play = field[1]
                
                # here we check mode
                if os.path.exists('/tmp/g2u_dictation'):
                    self.dictation = True
            except Exception:
                print 'Config file', self.config
                print 'missing...'
    
    # record the config
    def __recordconfig(self):
        try:
            with open(self.config, "w") as f:
                f.write('recording='+str(self.recording_time)+'\n')
                f.write('pause='+self.entry2.get_text()+'\n')
                f.write('play='+self.entry1.get_text()+'\n')
                f.write('locale='+self.locale+'\n')
                f.close()
        except Exception:
            print 'Config file', self.config
            print 'Unable to write'
    
    # get the grid        
    def getGrid(self):        
        return self.grid

    def scale_moved(self,event):
        self.recording_time = int(self.scale.get_value())
        self.__recordconfig()

    def dictation_state(self,button,active):
        if button.get_active() :
            f=open('/tmp/g2u_dictation',"w")
            f.close()
        else:
            if os.path.exists('/tmp/g2u_dictation'):
                os.remove('/tmp/g2u_dictation')

    def on_clicked(self,button):
        self.__recordconfig()
        #self.w.destroy()

    # return a combobox to add to the toolbar
    def __get_combobox(self):
        """
        @description: get the combobox of the toolbar
        
        @return: a Gtk.Combobox
        """
        # the data in the model, of type string
        locale_path = os.path.dirname(os.path.abspath(__file__))+'/../i18n'
        listmodel = Gtk.ListStore(str)
        # append the data in the model
        selected=0
        i=0
        self.LANG = {}
        for language in os.listdir(locale_path):
            if os.path.isdir(locale_path+'/'+language+'/LC_MESSAGES'):
                listmodel.append([language])
                self.LANG[i] = language
                if language == self.locale:
                    selected = i
                i+=1
                    
        # a combobox to see the data stored in the model
        combobox = Gtk.ComboBox(model=listmodel)
        combobox.set_tooltip_text(_("What language to choose")+'?')

        # a cellrenderer to render the text
        cell = Gtk.CellRendererText()

        # pack the cell into the beginning of the combobox, allocating
        # no more space than needed
        combobox.pack_start(cell, False)
        # associate a property ("text") of the cellrenderer (cell) to a column (column 0)
        # in the model used by the combobox
        combobox.add_attribute(cell, "text", 0)

        # the first row is the active one by default at the beginning
        combobox.set_active(selected)

        # connect the signal emitted when a row is selected to the callback function
        combobox.connect("changed", self.on_combochanged)
        return combobox

    def on_combochanged(self,combo):
        self.locale = str(self.LANG[combo.get_active()])
        self.__recordconfig()
