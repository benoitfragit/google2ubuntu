#!/usr/bin/env python
# -*- coding: utf-8 -*-
from subprocess import *
from os.path import expanduser
import sys, subprocess, os, json, urllib2, unicodedata, time, gettext, locale

from Googletts import tts
from stringParser import stringParser
from localehelper import LocaleHelper

# La classe interface permet de lancer l'enregistrement et de communiquer
# avec Google
class interface():
    """
    @description: This class start the osd server, then start recording your voice before
    asking Google for the translation. Then, the result is parsing in order to
    execute the associated action
    """
    def __init__(self, key):
        # make the program able to switch language
        self.p = os.path.dirname(os.path.abspath(__file__)).strip('librairy')

        localeHelper = LocaleHelper('en_EN')

        self.lang = localeHelper.getLocale()
        # this line can be remove if we modify the config/en_EN to config/en
        #self.lang = self.lang+'_'+self.lang.upper()

        # Initialisation des notifications
        self.PID = str(os.getpid())
        os.system('rm /tmp/g2u_*_'+self.PID+' 2>/dev/null')
        os.system('python '+self.p+'librairy/osd.py '+self.PID+' &')

        # on joue un son pour signaler le démarrage
        os.system('play '+self.p+'resources/sound.wav &')
        os.system('> /tmp/g2u_start_'+self.PID)

        # On lance le script d'enregistrement pour acquérir la voix pdt 5s
        command =self.p+'record.sh ' + self.PID
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output,error  = p.communicate()
        # return to 16kHz
        os.system(self.p+'convert.sh '+self.PID)
        self.sendto(key)

    def sendto(self, key):
        """
        @function: Send the flac file to Google and start the parser
        """
        # lecture du fichier audio
        filename='/tmp/voix_'+self.PID+'.flac'
        f = open(filename)
        data = f.read()
        f.close()

        # suppression du fichier audio
        if os.path.exists('/tmp/voix_'+self.PID+'.flac'):
            os.system('rm /tmp/voix_'+self.PID+'.flac')

        # fichier de configuration
        config = expanduser('~') + '/.config/google2ubuntu/google2ubuntu.xml'
        default = self.p +'config/'+self.lang+'/default.xml'

        if os.path.exists(config):
            config_file = config
        else:
            if os.path.exists(expanduser('~') +'/.config/google2ubuntu') == False:
                os.makedirs(expanduser('~') +'/.config/google2ubuntu')
            if os.path.exists(expanduser('~') +'/.config/google2ubuntu/modules') == False:
                os.system('cp -r '+self.p+'/modules '+expanduser('~') +'/.config/google2ubuntu')
            if os.path.exists(default) == False:
                default = self.p+'config/en_EN/default.xml'

            config_file = default

        print 'config file:', config_file
        print key
        try:
            # envoie une requête à Google
            #req = urllib2.Request('https://www.google.com/speech-api/v2/recognize?output=json&lang='+self.lang+'&key=AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw&client=chromium', data=data, headers={'Content-type': 'audio/x-flac; rate=16000'})
            req = urllib2.Request('https://www.google.com/speech-api/v2/recognize?output=json&lang='+self.lang+'&key='+key+'&client=chromium', data=data, headers={'Content-type': 'audio/x-flac; rate=16000'})
            # retour de la requête
            ret = urllib2.urlopen(req)
            response = ret.read()
            response = response.split('\n', 1)[1]
            text = response.split('"transcript":"',2)[1].split('"',2)[0]
            # parsing du retour
            #text=json.load(response)
            os.system('echo "'+text.encode("utf-8")+'" > /tmp/g2u_result_'+self.PID)
            
            # parsing du résultat pour trouver l'action
            sp = stringParser(text,config_file,self.PID)
        except Exception:
            message = _('unable to translate')
            os.system('echo "'+message+'" > /tmp/g2u_error_'+self.PID)
            sys.exit(1)
