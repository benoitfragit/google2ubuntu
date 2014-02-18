#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import expanduser
from subprocess import *
from Googletts import tts
import os, gettext, time, subprocess, unicodedata

gettext.install('google2ubuntu',os.path.dirname(os.path.abspath(__file__))+'/i18n/')

# Permet de faire appel aux modules    
class workWithModule():
    """
    @description: This class allows you to call external modules. If a call
    for an external module is detected by the parser then this class check
    the module's config file before extracting modules's parameter from the
    text you have pronounced
    """
    def __init__(self,module_path,module_name,text,linker,plus,PID):
        self.pid = PID
        
        try:
            # on utilise un mot de liaison pour séparer l'appel du module
            # des arguments à lui envoyer
            # ex: Quelle est la météo à Paris
            #     Quelle est la météo à Issy les moulineaux
            #
            # Le mot de liaison peut être " à "
            sentence=text.lower()
            sentence=unicodedata.normalize('NFKD', text)
            sentence=sentence.lower()  

            if sentence.count(linker) > 0:
                param =(sentence.split(linker,1)[1]).encode("utf-8")

                # on regarde si l'utilisateur veut transformer les ' ' en +
                if plus == '1':
                    param=param.replace(' ','+')
                
                # commande qui sera exécutée    
                execute = expanduser('~')+'/.config/google2ubuntu/modules/'+module_name+' '+'"'+param+'" &'
                os.system(execute)
            else:
                message=_("you didn't say the linking word")   
                os.system('echo "'+message+'" > /tmp/g2u_error_'+self.pid)      
            
        except IOError:
            message = _('args file missing')
            os.system('echo "'+message+'" > /tmp/g2u_error_'+self.pid)
            sys.exit(1) 
