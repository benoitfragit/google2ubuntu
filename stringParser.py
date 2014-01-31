#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import expanduser
from Notification import notification
from workWithModule import workWithModule
from basicCommands import basicCommands
from Googletts import tts
import os, gettext, time
gettext.install('google2ubuntu',os.path.dirname(os.path.abspath(__file__))+'/i18n/')

# Permet d'exécuter la commande associée à un mot prononcé
class stringParser():
    def __init__(self,text,file,notif):
        # read configuration files
        try:
            # ouverture du fichier en lecture
            f=open(file,"r")
            max = 0;
            keys=[]
            actions=[]
            do = ''

            # Pour chaque ligne du fichier de config, on obtient le couple
            # clé/commande
            for ligne in f:
                k,a = self.getKeyAction(ligne)
                if k is not 'error':
                    keys.extend([k])
                    actions.extend([a])        
            
            f.close();
            
            # Pour chaque couple clé/commande, on parse la clé pour prendre en
            # compte les choix minuscules et majuscules compris entre []
            for i in range(len(keys)):
                tab = self.getAllKeys(keys[i])
                # on attribue un score à chaque key suivant sa proximité avec
                # la phrase prononcée, on ne garde que l'action qui est à le 
                # score le plus élevé
                score = 0;
                for j in range(len(tab)):
                    score += text.count(unicode(tab[j],"utf-8"))
                    # j'ai déjà eu des problèmes ici d'ou le unicode
                        
                if max < score:
                    max = score
                    do = actions[i]
            
            # on regarde si la commande fait appel à un module
            # si oui, alors on lui passe en paramètre les dernier mots prononcé
            # ex: si on prononce "quelle est la météo à Paris"
            # la ligne de configuration dans le fichier est: [q/Q]uelle*météo=/modules/weather/weather.sh
            # on coupe donc l'action suivant '/'
            check = do.split('/')
            if _('modules') in check:
                # si on trouve le mot "modules", on instancie une classe workWithModule et on lui passe
                # le dossier ie weather, search,...; le nom du module ie weather.sh, search.sh et le texte prononcé
                wm = workWithModule(check[2],check[3],text,notif)
            elif _('internal') in check:
                # on execute une commande intene, la commande est configurée
                # ainsi interne/batterie, on envoie batterie à la fonction
                b = basicCommands(check[1],notif)
            else:
                # on exécute directement l'action
                os.system(do)
            
            time.sleep(1)
            notif.close()
            
        except IOError:
            notif.update(_('Error'),_('Setup file missing'),'ERROR')
            tts(_('Error')+' '+_('Setup file missing'))
            time.sleep(3)
            notif.close()            
            sys.exit(1)   
            
    
    def getKeyAction(self,line):
        #supprimer le caractere de fin de ligne
        data=line.rstrip('\n\r')
        if len(data) >= 2:    
            keys = data.split('=')[0]
            actions = data.split('=')[1]
            # retourne un couple clé, action
            return keys,actions;
        else:
            return 'error','error'
                       
    def getAllKeys(self,key):
        #extraction des mots
        tab = []
        # get all words
        # suppression des * en début et fin
        key = key.strip('*')
        # on ne garde que les mots utiles
        Key = key.split('*')
        for var in Key:
            var = var.strip('[')
            tmp = var.split(']')
            if len(tmp) > 1:
                endw = tmp[1]
                for e in tmp[0].split('/'):
                   tab.extend([e+endw])
            else:
                tab.extend([tmp[0]])
                
        return tab   
