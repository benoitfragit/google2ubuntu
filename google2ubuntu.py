#!/usr/bin/env python
# -*- coding: utf-8 -*-
from subprocess import *
from os.path import expanduser
import sys, subprocess, os, json, urllib2, unicodedata, time, gettext, locale

sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/librairy')

from Googletts import tts
from stringParser import stringParser

PID = str(os.getpid())
lang = locale.getlocale()[0]
if os.path.isdir(os.path.dirname(os.path.abspath(__file__))+'/i18n/'+lang.split('_')[0]) == False:
    lang='en_EN'

gettext.install('google2ubuntu',os.path.dirname(os.path.abspath(__file__))+'/i18n/')

# La classe interface permet de lancer l'enregistrement et de communiquer
# avec Google
class interface():
    def __init__(self):
        # on joue un son pour signaler le démarrage
        os.system('play '+os.path.dirname(os.path.abspath(__file__))+'/resources/sound.wav &')
        os.system('> /tmp/g2u_start_'+PID)

        # On lance le script d'enregistrement pour acquérir la voix pdt 5s
        command =os.path.dirname(os.path.abspath(__file__))+'/record.sh ' + PID
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output,error  = p.communicate()

        self.sendto()    

    def sendto(self):
        # lecture du fichier audio
        filename='/tmp/voix_'+PID+'.flac'
        f = open(filename)
        data = f.read()
        f.close()
        
        # suppression du fichier audio
        if os.path.isfile('/tmp/voix_'+PID+'.flac'):
            os.system('rm /tmp/voix_'+PID+'.flac')
        
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
        
        print 'config file:', config_file
        try:
            # envoie une requête à Google
            req = urllib2.Request('https://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&lang='+lang, data=data, headers={'Content-type': 'audio/x-flac; rate=16000'})  
            # retour de la requête
            ret = urllib2.urlopen(req)
            
            # parsing du retour
            text=json.loads(ret.read())['hypotheses'][0]['utterance']
            os.system('echo "'+text.encode("utf-8")+'" > /tmp/g2u_result_'+PID)

            # parsing du résultat pour trouver l'action
            sp = stringParser(text,config_file,PID)                 
        except Exception:
            message = _('unable to translate')
            os.system('echo "'+message+'" > /tmp/g2u_error_'+PID)
            sys.exit(1)

# Initialisation des notifications
os.system('rm /tmp/g2u* 2>/dev/null')
os.system('python '+os.path.dirname(os.path.abspath(__file__))+'/librairy/osd.py '+PID+' &')
g2u = interface()
