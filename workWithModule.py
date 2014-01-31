#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import expanduser
from subprocess import *
from Notification import notification
from Googletts import tts
import os, gettext, time, subprocess

gettext.install('google2ubuntu',os.path.dirname(os.path.abspath(__file__))+'/i18n/')

# Permet de faire appel aux modules    
class workWithModule():
    def __init__(self,module_path,module_name,text,notif):
        try:
            # Lecture du fichier de configuration du module
            argsfile=expanduser('~')+'/.config/google2ubuntu/modules/'+module_path+'/args';
            print argsfile
            f = open(argsfile,'r')
            ligne=(f.readline()).rstrip('\n\r')  
            linker=unicode(ligne.split('=')[1],"utf-8")
            ligne=(f.readline()).rstrip('\n\r')              
            plus=ligne.split('=')[1] 
            f.close()  

            # on utilise un mot de liaison pour séparer l'appel du module
            # des arguments à lui envoyer
            # ex: Quelle est la météo à Paris
            #     Quelle est la météo à Issy les moulineaux
            #
            # Le mot de liaison peut être " à "
            print text
            if text.count(linker) > 0:
                param =(text.split(linker)[1]).encode("utf-8")
                
                # on regarde si l'utilisateur veut transformer les ' ' en +
                if plus == 1:
                    param=param.replace(' ','+')
                
                # commande qui sera exécutée    
                
                execute = expanduser('~') +'/.config/google2ubuntu/modules/'+module_path+'/'+module_name+' '+param
                os.system(execute)
                tts (_('Search results for')+' '+param)
            else:
                notif.update(_('Error'),_("you didn't say the linking word")+'\n'+linker,'ERROR')    
                tts(_('Error')+' '+_("you didn't say the linking word"))
                time.sleep(3)
                notif.close()        
            
        except IOError:
            notif.update(_('Error'),_('args file missing'),'ERROR')
            tts(_('Error')+' '+-('args file missing'))
            time.sleep(3)
            notif.close()
            sys.exit(1) 
