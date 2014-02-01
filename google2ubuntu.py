#!/usr/bin/env python
# -*- coding: utf-8 -*-
from subprocess import *
from os.path import expanduser
import sys, subprocess, os, json, urllib2, unicodedata, time, gettext, locale

sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/librairy')

from Googletts import tts
from Notification import notification
from stringParser import stringParser

PID = os.getpid()
lang = locale.getlocale()[0]
gettext.install('google2ubuntu',os.path.dirname(os.path.abspath(__file__))+'/i18n/')

# La classe interface permet de lancer l'enregistrement et de communiquer
# avec Google
class interface():
    def __init__(self):
        notif = notification('Google2Ubuntu',_('Ready'))
        # on joue un son pour signaler le démarrage
        os.system('play '+os.path.dirname(os.path.abspath(__file__))+'/resources/sound.wav &')
        notif.update(_('Recording')+':',_('Processing'),'RECORD')
        # On lance le script d'enregistrement pour acquérir la voix pdt 5s
        command =os.path.dirname(os.path.abspath(__file__))+'/record.sh ' + str(PID)
        #p = subprocess.check_call([command])  
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output,error  = p.communicate()
        notif.update(_("End of recording"),_('Sending to Google'),'NETWORK')
        self.sendto(notif)    

    def sendto(self,notif):
        # lecture du fichier audio
        filename='/tmp/voix_'+str(PID)+'.flac'
        f = open(filename)
        data = f.read()
        f.close()
        
        # suppression du fichier audio
        if os.path.isfile('/tmp/voix_'+str(PID)+'.flac'):
            os.system('rm /tmp/voix_'+str(PID)+'.flac')
        
        # fichier de configuration
        config = expanduser('~') + '/.config/google2ubuntu/google2ubuntu.xml'
        default = os.path.dirname(os.path.abspath(__file__))+'/config/default.xml'
        
        if os.path.exists(config):
            config_file = config
        else:
            if os.path.exists(expanduser('~') +'/.config/google2ubuntu') == False:
                os.makedirs(expanduser('~') +'/.config/google2ubuntu')
                os.system('cp -r /usr/share/google2ubuntu/modules '+expanduser('~') +'/.config/google2ubuntu')    
                
            config_file = default
        
        try:
            # envoi d'une requête à Google
            req = urllib2.Request('https://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&lang='+lang, data=data, headers={'Content-type': 'audio/x-flac; rate=16000'})  
            # retour de la requête
            ret = urllib2.urlopen(req)
            
            # parsing du retour
            result=json.loads(ret.read())['hypotheses']

            # si on a un résultat
            text = result[0]['utterance']
            notif.update(_("Searching action associated to")+':',text,'EXECUTE')
                    
            # parsing du résultat pour trouver l'action
            sp = stringParser(text,config_file,notif)    
        except Exception:
            notif.update(_('Error'),_('Unable to translate'),'ERROR') 
            time.sleep(3)
            notif.close()
            sys.exit(1)

# Initialisation des notifications
g2u = interface()
