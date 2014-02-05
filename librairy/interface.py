#!/usr/bin/env python
# -*- coding: utf-8 -*-
from subprocess import *
from os.path import expanduser
import sys, subprocess, os, json, urllib2, unicodedata, time, gettext, locale

from Googletts import tts
from stringParser import stringParser

lang = locale.getlocale()[0]
gettext.install('google2ubuntu',os.path.dirname(os.path.abspath(__file__))+'/i18n/')

# La classe interface permet de lancer l'enregistrement et de communiquer
# avec Google
class interface():
    """
    @description: This class start the osd server, then start recording your voice before
    asking Google for the translation. Then, the result is parsing in order to
    execute the associated action
    """
    def __init__(self):
        # Initialisation des notifications
        self.PID = str(os.getpid())
        self.p = os.path.dirname(os.path.abspath(__file__)).strip('librairy')
        os.system('rm /tmp/g2u_*_'+self.PID+' 2>/dev/null')
        os.system('python '+self.p+'librairy/osd.py '+self.PID+' &')

        # on joue un son pour signaler le démarrage
        os.system('play '+self.p+'resources/sound.wav &')
        os.system('> /tmp/g2u_start_'+self.PID)

        # On lance le script d'enregistrement pour acquérir la voix pdt 5s
        command =self.p+'record.sh ' + self.PID
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output,error  = p.communicate()

        self.sendto()    

    def sendto(self):
        """
        @function: Send the flac file to Google and start the parser
        """
        # lecture du fichier audio
        filename='/tmp/voix_'+self.PID+'.flac'
        f = open(filename)
        data = f.read()
        f.close()
        
        # suppression du fichier audio
        if os.path.isfile('/tmp/voix_'+self.PID+'.flac'):
            os.system('rm /tmp/voix_'+self.PID+'.flac')
        
        # fichier de configuration
        config = expanduser('~') + '/.config/google2ubuntu/google2ubuntu.xml'
        default = self.p +'config/'+lang+'/default.xml'
        
        if os.path.exists(config):
            config_file = config
        else:
            if os.path.exists(expanduser('~') +'/.config/google2ubuntu') == False:
                os.makedirs(expanduser('~') +'/.config/google2ubuntu')
                os.system('cp -r /usr/share/google2ubuntu/modules '+expanduser('~') +'/.config/google2ubuntu')    
            if os.path.exists(default) == False:
                default = self.p+'config/en_EN/default.xml'
                
            config_file = default
        
        print 'config file:', config_file
        try:
            # envoie une requête à Google
            req = urllib2.Request('https://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&lang='+lang, data=data, headers={'Content-type': 'audio/x-flac; rate=16000'})  
            # retour de la requête
            ret = urllib2.urlopen(req)
            
            # parsing du retour
            text=json.loads(ret.read())['hypotheses'][0]['utterance']
            os.system('echo "'+text.encode("utf-8")+'" > /tmp/g2u_result_'+self.PID)

            # parsing du résultat pour trouver l'action
            sp = stringParser(text,config_file,self.PID)                 
        except Exception:
            message = _('unable to translate')
            os.system('echo "'+message+'" > /tmp/g2u_error_'+self.PID)
            sys.exit(1)
