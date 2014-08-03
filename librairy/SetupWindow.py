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
    def __init__(self,button_back, button_cancel):
        # class variables
        localeHelper = LocaleHelper('en_EN')
        self.locale = localeHelper.getLocale()
        self.recording_time = 5
        self.player_pause = ''
        self.player_play = ''
        self.dictation = False
        self.config = expanduser('~')+'/.config/google2ubuntu/google2ubuntu.conf'
        self.threshold = 5
        self.key = ''
        self.hotword = _('ok start')
        
        # looking for the configuration file
        self.__loadconfig()

        label0=Gtk.Label(_('Set Google Api Key'))
        label0.set_justify(Gtk.Justification.LEFT)
        label0.set_halign(Gtk.Align.START)
        label1=Gtk.Label(_('Select your language'))
        label1.set_justify(Gtk.Justification.LEFT)
        label1.set_halign(Gtk.Align.START)
        label1.set_hexpand(True)
        label2=Gtk.Label(_('Set the recording time (seconds)'))
        label2.set_justify(Gtk.Justification.LEFT) 
        label2.set_halign(Gtk.Align.START) 
        label3=Gtk.Label(_("Set the music player's play command"))
        label3.set_justify(Gtk.Justification.LEFT) 
        label3.set_halign(Gtk.Align.START) 
        label4=Gtk.Label(_("Set the music player's pause command"))
        label4.set_justify(Gtk.Justification.LEFT) 
        label4.set_halign(Gtk.Align.START) 
        label5=Gtk.Label(_('Hotword mode'))
        label5.set_justify(Gtk.Justification.LEFT) 
        label5.set_halign(Gtk.Align.START) 
        label6=Gtk.Label(_('Set the noise threshold'))
        label6.set_justify(Gtk.Justification.LEFT) 
        label6.set_halign(Gtk.Align.START)         
        label7 = Gtk.Label(_('Set the hotword'))
        label7.set_justify(Gtk.Justification.LEFT) 
        label7.set_halign(Gtk.Align.START) 
        
        combo = self.__get_combobox()
        
        self.scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL,1,10,1)
        self.scale.set_value(self.recording_time)
        self.scale.connect("value-changed", self.scale_moved)
        self.scale.set_tooltip_text(_('Change the recording time'))
        
        self.entry0 = Gtk.Entry()
        self.entry0.set_text(self.key)    
        self.entry0.set_tooltip_text(_('Set the Google Api Key'));
        
        self.entry1 = Gtk.Entry()
        self.entry1.set_text(self.player_play)
        self.entry1.set_tooltip_text(_('Set the play command'))
        
        
        self.entry2 = Gtk.Entry()
        self.entry2.set_text(self.player_pause)
        self.entry2.set_tooltip_text(_('Set the pause command'))

        switch_active = Gtk.Switch()
        switch_active.set_active(False)
        switch_active.set_hexpand(False)
        if os.path.exists('/tmp/hotword'):
            switch_active.set_active(True)
            
        switch_active.set_tooltip_text(_('Put the hotword mode ON or OFF'))
        switch_active.connect("notify::active", self.active_hotword)

        self.scale_threshold = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL,1,20,0.5)
        self.scale_threshold.set_value(self.threshold)
        self.scale_threshold.connect("value-changed",self.threshold_changed)
        self.scale_threshold.set_tooltip_text(_('Set the sound level in % under which sound is considerated as noise'))

        self.entry3 = Gtk.Entry()
        self.entry3.set_text(self.hotword)
        self.entry3.set_tooltip_text(_('Set the hotword to start effective recording'))
        
        button_back.connect("clicked",self.on_clicked)
                
        # an invisble widget to fill the window
        ll = Gtk.Label()
        ll.set_vexpand(True)
        
        self.grid = Gtk.Grid()
        self.grid.set_border_width(10)
        self.grid.set_row_spacing(15)
        self.grid.set_vexpand(True)
        self.grid.set_hexpand(True)
        self.grid.set_column_spacing(2)
        self.grid.set_column_homogeneous(False)
        self.grid.attach(label1,0,0,14,1)
        self.grid.attach(combo,14,0,1,1)
        self.grid.attach(label2,0,1,11,1)
        self.grid.attach(self.scale, 11,1,4,1)
        self.grid.attach(label3,0,2,11,1)
        self.grid.attach(self.entry1,11,2,4,1)
        self.grid.attach(label4,0,3,11,1)
        self.grid.attach(self.entry2,11,3,4,1)
        self.grid.attach(label5,0,4,14,1)
        self.grid.attach(switch_active,14,4,1,1)
        self.grid.attach(label7,0,5,11,1)
        self.grid.attach(self.entry3,11,5,4,1)
        self.grid.attach(label6,0,6,11,1)
        self.grid.attach(self.scale_threshold,11,6,4,1)
        self.grid.attach(label0, 0, 7, 11, 1)
        self.grid.attach(self.entry0, 11, 7, 4, 1)        
        self.grid.attach(ll,0,8,15,1)
        self.grid.attach(button_cancel,13,9,1,1)
        self.grid.attach(button_back,14,9,1,1) 
       
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
                                self.player_pause = field[1].replace('"','')
                            elif field[0] == 'play':
                                self.player_play = field[1].replace('"','')
                            elif field[0] == 'hotword':
                                self.hotword = field[1].replace('"','')
                            elif field[0] == 'threshold':
                                self.threshold = int(field[1])
                            elif field[0] == 'key':
                                self.key = field[1].replace('"','')
                
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
                f.write('pause="'+self.entry2.get_text()+'"\n')
                f.write('play="'+self.entry1.get_text()+'"\n')
                f.write('locale='+self.locale+'\n')
                f.write('hotword="'+self.entry3.get_text()+'"\n')
                f.write('threshold='+str(self.threshold)+'\n')
                f.write('key="'+self.entry0.get_text()+'"\n')
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

    def threshold_changed(self,event):
        self.threshold = int(self.scale_threshold.get_value())
        self.__recordconfig()
    
    def active_hotword(self,button,active):
        if button.get_active():
            p = os.path.dirname(os.path.abspath(__file__)).strip('librairy')
            os.system('bash '+p + 'listen.sh &')
        else:
            if os.path.exists('/tmp/hotword'):
                os.remove('/tmp/hotword')

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
