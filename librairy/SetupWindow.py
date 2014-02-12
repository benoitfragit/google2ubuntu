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
    def __init__(self):
        # class variables
        localeHelper = LocaleHelper('en_EN')
        self.locale = localeHelper.getLocale()
        self.recording_time = 5
        self.player_pause = 'undefine'
        self.player_play = 'undefine'
        self.dictation = False
        self.config = expanduser('~')+'/.config/google2ubuntu/google2ubuntu.conf'
        
        # looking for the configuration file
        self.__loadconfig()
        
        # build the window
        self.w = Gtk.Window()
        self.w.set_title(_("Setup window"))
        self.w.set_resizable(False)     
        self.w.get_focus()
        self.w.set_position(Gtk.WindowPosition.CENTER)      
        self.w.set_default_size(80,80)  
        self.w.set_border_width(5)
        self.w.set_hexpand(True)
        self.w.set_vexpand(True)

        # add the grid to the window        
        grid = self.__getGrid()
        self.w.add(grid)
        self.w.show_all()
    
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
                f.write('pause='+self.player_pause+'\n')
                f.write('play='+self.player_play+'\n')
                f.write('locale='+self.locale+'\n')
                f.close()
        except Exception:
            print 'Config file', self.config
            print 'Unable to write'
    
    # get the grid        
    def __getGrid(self):
        label1=Gtk.Label(_('Select your language'))
        label1.set_justify(Gtk.Justification.LEFT)
        label1.set_halign(Gtk.Align.START)
        label2=Gtk.Label(_('Set the recording time (seconds)'))
        label2.set_justify(Gtk.Justification.LEFT) 
        label2.set_halign(Gtk.Align.START) 
        label4=Gtk.Label(_("Set the music player's play command"))
        label4.set_justify(Gtk.Justification.LEFT) 
        label4.set_halign(Gtk.Align.START) 
        label5=Gtk.Label(_("Set the music palyer's pause command"))
        label5.set_justify(Gtk.Justification.LEFT) 
        label5.set_halign(Gtk.Align.START) 
        
        combo = self.__get_combobox()
        
        self.scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL,1,10,1)
        self.scale.set_value(self.recording_time)
        self.scale.connect("value-changed", self.scale_moved)
        self.scale.set_tooltip_text(_('Change the recording time'))
                
        entry1 = Gtk.Entry()
        entry1.set_text(self.player_play)
        entry1.set_tooltip_text(_('Set the play command'))
        entry1.connect("activate", self.entry1_activate)
        
        entry2 = Gtk.Entry()
        entry2.set_text(self.player_pause)
        entry2.set_tooltip_text(_('Set the pause command'))
        entry2.connect("activate", self.entry2_activate)
        image = Gtk.Image()
        image.set_from_stock(Gtk.STOCK_APPLY, Gtk.IconSize.BUTTON)
        button = Gtk.Button(label="", image=image)
        button.connect("clicked",self.on_clicked)
        
        hs1 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hs2 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        grid = Gtk.Grid()
        grid.set_row_spacing(10)
        grid.set_column_spacing(5)
        grid.set_column_homogeneous(True)
        grid.attach(label1,0,0,5,1)
        grid.attach(combo,5,0,1,1)
        grid.attach(hs1,0,1,6,1)
        grid.attach(label2,0,2,6,1)
        grid.attach(self.scale, 0,3,6,1)
        grid.attach(hs2,0,4,6,1)
        grid.attach(label4,0,5,6,1)
        grid.attach(entry1,0,6,6,1)
        grid.attach(label5,0,7,6,1)
        grid.attach(entry2,0,8,6,1)
        grid.attach(button,5,9,1,1)
        return grid

    def scale_moved(self,event):
        self.recording_time = int(self.scale.get_value())
        self.__recordconfig()

    def entry1_activate(self,entry):
        self.player_play = entry.get_text()
        self.__recordconfig()
    
    def entry2_activate(self,entry):
        self.player_pause = entry.get_text()
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
        self.w.destroy()

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
