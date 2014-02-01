#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import expanduser
from Notification import notification
from workWithModule import workWithModule
from basicCommands import basicCommands
from Googletts import tts
import xml.etree.ElementTree as ET
import os, gettext, time, sys
gettext.install('google2ubuntu',os.path.dirname(os.path.abspath(__file__))+'/i18n/')

# Permet d'exécuter la commande associée à un mot prononcé
class stringParser():
    def __init__(self,text,File,notif):
        # read configuration files
        try:
            max = 0
            text=text.lower()
            tree = ET.parse(File)
            root = tree.getroot()
        
            tp = ''
            for entry in root.findall('entry'):
                score = 0
                Type=entry.get('name')
                Key=entry.find('key').text
                Command=entry.find('command').text
                key=Key.split(' ')
                for j in range(len(key)):
                    score += text.count(key[j])
                        
                if max < score:
                    max = score
                    do = Command
                    tp = Type
            
            # on regarde si la commande fait appel à un module
            # si oui, alors on lui passe en paramètre les dernier mots prononcé
            # ex: si on prononce "quelle est la météo à Paris"
            # la ligne de configuration dans le fichier est: [q/Q]uelle*météo=/modules/weather/weather.sh
            # on coupe donc l'action suivant '/'
            if _('modules') in tp:
                check = do.split('/')
                # si on trouve le mot "modules", on instancie une classe workWithModule et on lui passe
                # le dossier ie weather, search,...; le nom du module ie weather.sh, search.sh et le texte prononcé
                wm = workWithModule(check[0],check[1],text,notif)
            elif _('internal') in tp:
                # on execute une commande intene, la commande est configurée
                # ainsi interne/batterie, on envoie batterie à la fonction
                b = basicCommands(do,notif)
            elif _('external') in tp:
                # on exécute directement l'action
                os.system(do)
            
            notif.close()
            
        except IOError:
            notif.update(_('Error'),_('Setup file missing'),'ERROR')
            tts(_('Error')+' '+_('Setup file missing'))
            time.sleep(3)
            notif.close()            
            sys.exit(1)   
