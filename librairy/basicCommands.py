#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gi.repository import Gtk
from gi.repository import Gdk
from subprocess import *
from Googletts import tts
import os, gettext, time, subprocess

gettext.install('google2ubuntu',os.path.dirname(os.path.abspath(__file__))+'/i18n/')

# Permet de faire appel aux fonctions basiques
class basicCommands():
    def __init__(self,text,PID):
        # suivant le paramètre reçu, on exécute une action
        self.pid = PID
        if text == _('time'):
            self.getTime()
        elif text == _('power'):
            self.getPower()
        elif text == _('clipboard'):
            self.read_clipboard()
        else:
            print "no action found"
    
    def read_clipboard(self):
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)

        text = clipboard.wait_for_text()
        if text != None:
            text=text.replace("'",' ')
            print text
            tts(text)
        else:
            tts(_('Nothing in the clipboard'))
    
    def getTime(self):
        var=time.strftime('%d/%m/%y %H:%M',time.localtime())
        print var
        os.system('echo "'+var+'" > /tmp/g2u_display_'+self.pid)
                    
    def getPower(self):
        command = "acpi -b"
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output,error  = process.communicate()
        #parsing output
        if output.count('Battery') > 0:
            pcent = output.split(' ')[3]
            rtime = output.split(' ')[4]
            
            if output.count('Charging') > 0:
                message = _('Charging')+': '+pcent+'\n'+rtime+' '+_('before charging')
            else:
                message = _('Discharging')+': '+pcent+'\n'+rtime+' '+_('remaining')
        else:
            message = _('battery is not plugged')
        
        os.system('echo "'+message+'" > /tmp/g2u_display_'+self.pid)
        tts(message)
