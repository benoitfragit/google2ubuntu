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
        grid = self.__getGrid()
        
        # add the grid to the window
    
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

S=SetupWindow()
