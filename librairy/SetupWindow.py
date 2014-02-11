#!/usr/bin/env python
# -*- coding: utf-8 -*-  
from gi.repository import Gtk
from gi.repository import Notify
from gi.repository import Gdk
from gi.repository import Gio
from os.path import expanduser
import os, sys, gettext

class SetupWindow():
    def __init__(self):
        # class variables
        self.recording_time = 5
        self.player_pause = 'undef'
        self.player_play = 'undef'
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
                f.write('recording='+self.recording_time+'\n')
                f.write('pause='+self.player_pause+'\n')
                f.write('play='+self.play+'\n')
        except Exception:
            print 'Config file', self.config
            print 'Unable to write'
    
    # get the grid        
    def __getGrid(self):
        print "get the grid"
        label1=Gtk.Label(_('Set the recording time'))
        label2=Gtk.Label(_('Set the mode'))
        label3=Gtk.Label(_("Set the music player's play command"))
        label4=Gtk.Label(_("Set the music palyer's pause command"))
        
        scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL,1,10,1)
        switch = Gtk.Switch()
        entry1 = Gtk.Entry()
        entry2 = Gtk.Entry()
        button = Gtk.Button.new_from_stock(Gtk.STOCK_OK)
        
        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        grid.attach(label1,0,0,6,1)
        grid.attach(scale, 0,1,6,1)
        grid.attach(label2,0,2,5,1)
        grid.attach(switch,5,2,1,1)
        grid.attach(label3,0,3,6,1)
        grid.attach(entry1,0,4,6,1)
        grid.attach(label4,0,5,6,1)
        grid.attach(entry2,0,6,6,1)
        grid.attach(button,5,7,1,1)
        return grid
