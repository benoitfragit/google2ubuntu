#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Notify
from os.path import expanduser
from localehelper import LocaleHelper
import time, os, gettext, sys, locale

path = os.path.dirname(os.path.abspath(__file__)).strip('librairy')
localeHelper = LocaleHelper()
lang = localeHelper.getLocale()
t=gettext.translation('google2ubuntu',path+'i18n/',languages=[lang])
t.install()

#keep the old way for the moment
#gettext.install('google2ubuntu',path+'/i18n/')
RESULT = False
path += 'resources'


if len(sys.argv) >= 2:
    PID = sys.argv[1]
    # nom des fichiers
    start='/tmp/g2u_start_'+PID
    stop='/tmp/g2u_stop_'+PID
    result='/tmp/g2u_result_'+PID
    cmd='/tmp/g2u_cmd_'+PID
    error='/tmp/g2u_error_'+PID
    display='/tmp/g2u_display_'+PID


    # initialisation
    Notify.init("google2ubuntu")
    n = Notify.Notification.new('google2ubuntu',_('Ready'),path+"/icons.png")
    n.set_urgency(Notify.Urgency.CRITICAL)    
    n.show()

    while os.path.exists(start) == False:
        n.update('google2ubuntu',_('Ready'), path+"/icons.png")
        n.show()
        time.sleep(0.5)

    i = 0    
    delay=0.1
    while os.path.exists(stop) == False:
        if os.path.exists(error):
            f = open(error,"r")
            title = _('Error')
            body = f.readline().rstrip('\n')
            f.close
            n.update(title, body,icon = path+"/error.png")
            n.show()
            time.sleep(2)
            n.close()
            os.system('rm /tmp/g2u_*_'+PID+' 2>/dev/null')
            sys.exit(1)
            
        if os.path.exists(result) and RESULT == False:
            f = open(result,"r")
            title=_('Recognition result')
            body = f.readline().rstrip('\n')
            icon = path+"/icons.png"
            f.close()
            delay = 2
            RESULT = True
        elif os.path.exists(cmd) and RESULT == True:
            if os.path.exists(result):
                os.system('rm '+result)
            f = open(cmd,"r")
            title = _('Calling command')
            body = f.readline().rstrip('\n')
            icon = path+"/icons.png"
            delay = 2
            f.close()
        elif os.path.exists(display):
            f = open(display,"r")
            title = _('Information')
            body = f.readline().rstrip('\n')
            f.close
            icon = path+"/icons.png"
            delay=3
        else:
            title = _('Performing recording')
            body = _('Please speak')
            icon = path+"/Waiting/wait-"+str(i)+".png"
    
        n.update(title, body, icon)
        n.show()
        time.sleep(delay)
        i += 1;
        if i > 17:
            i = 0    

    n.update("google2ubuntu",_('Done'),path+"/icons.png")
    n.show()
    time.sleep(1)
    n.close()
    os.system('rm /tmp/g2u_*_'+PID+' 2>/dev/null')
