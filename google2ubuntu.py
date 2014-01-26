# -*- coding: utf-8 -*-  
#!/usr/bin/env python
from subprocess import *
from gi.repository import Gtk
from gi.repository import Notify
from os.path import expanduser
import sys
import subprocess 
import os
import json
import urllib2
import time

# Cette classe utilis Notify pour alerter l'utilisateur
class notification():
    # initialisation du serveur de notification
    def __init__(self,titre,corps):
        Notify.init(titre)
        self.n = Notify.Notification.new(titre,corps,"")
        self.n.set_urgency(Notify.Urgency.CRITICAL)    
        self.n.set_icon_from_pixbuf(Gtk.Label().render_icon(Gtk.STOCK_MEDIA_PLAY, Gtk.IconSize.DIALOG))
        self.n.show()
        time.sleep(0.5)

    # on mets à jours la notification
    def update(self,titre,text,typeicon):
        self.n.update(titre,text,"")
        if typeicon == 'RECORD':
            self.n.set_icon_from_pixbuf(Gtk.Label().render_icon(Gtk.STOCK_MEDIA_RECORD, Gtk.IconSize.DIALOG))
        elif typeicon == 'NETWORK':
            self.n.set_icon_from_pixbuf(Gtk.Label().render_icon(Gtk.STOCK_MEDIA_RECORD, Gtk.IconSize.DIALOG))
        elif typeicon == 'EXECUTE':
            self.n.set_icon_from_pixbuf(Gtk.Label().render_icon(Gtk.STOCK_EXECUTE, Gtk.IconSize.DIALOG))
        elif typeicon == 'ERROR':
            self.n.set_icon_from_pixbuf(Gtk.Label().render_icon(Gtk.STOCK_DIALOG_ERROR, Gtk.IconSize.DIALOG))   
        else:
            self.n.set_icon_from_pixbuf(Gtk.Label().render_icon(Gtk.STOCK_INFO, Gtk.IconSize.DIALOG))    
        
        self.n.show()
    
    # on quitte
    def close(self):
        self.n.close()

# La classe interface permet de lancer l'enregistrement et de communiquer
# avec Google
class interface():
    def __init__(self):
        # on joue un son pour signaler le démarrage
        os.system('aplay '+os.path.dirname(os.path.abspath(__file__))+'/sound.wav')
        notif.update('Enregistrement:','En cours','RECORD')
        
        # On lance le script d'enregistrement pour acquérir la voix pdt 5s
        command =os.path.dirname(os.path.abspath(__file__))+'/record.sh'
        p = subprocess.check_call([command])  
        
        notif.update("Fin de l'enregistrement",'Envoi à Google','NETWORK')
        self.sendto()    

    def sendto(self):
        # lecture du fichier audio
        filename='/tmp/voix.flac'
        f = open(filename)
        data = f.read()
        f.close()
        
        # envoi d'une requête à Google
        req = urllib2.Request('https://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&lang=fr-FR', data=data, headers={'Content-type': 'audio/x-flac; rate=16000'})
        try:
            # retour de la requête
            ret = urllib2.urlopen(req)
            try:
                # parsing du retour
                result=json.loads(ret.read())['hypotheses']
                if len(result) != 0:
                    # si on a un résultat
                    text = result[0]['utterance']
                    notif.update("Recherche de l'action associee à:",text,'EXECUTE')
                    
                    # fichier de configuration
                    config = expanduser('~') + '/.config/google2ubuntu/google2ubuntu.conf'
                    
                    # parsing du résultat pour trouver l'action
                    sp = stringParser(text,config)
                else:
                    notif.update('Erreur','Je ne comprends pas ce que vous dites','ERROR')
                    time.sleep(3)
                    notif.close()
                    sys.exit(1)                
                    
            except ValueError, IndexError:
                notif.update('Erreur','Traduction impossible','ERROR')
                time.sleep(3)
                notif.close()
                sys.exit(1)
                
        except urllib2.URLError:
            notif.update('Erreur','Envoi à Google impossible','ERROR')    
            time.sleep(3)
            notif.close()
            sys.exit(1)

# Permet d'exécuter la commande associée à un mot prononcé
class stringParser():
    def __init__(self,text,file):
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
            if 'modules' in check:
                # si on trouve le mot "modules", on instancie une classe workWithModule et on lui passe
                # le dossier ie weather, search,...; le nom du module ie weather.sh, search.sh et le texte prononcé
                wm = workWithModule(check[2],check[3],text)
            elif 'interne' in check:
                # on execute une commande intene, la commande est configurée
                # ainsi interne/batterie, on envoie batterie à la fonction
                b = basicCommands(check[1])
            else:
                # on exécute directement l'action
                os.system(do)
            
            time.sleep(1)
            notif.close()
            
        except IOError:
            notif.update('Erreur','Lecture du fichier de config impossible','ERROR')
            time.sleep(3)
            notif.close()            
            sys.exit(1)   
            
    
    def getKeyAction(self,line):
        #supprimer le caractere de fin de ligne
        data=line.rstrip('\n\r')    
        keys = data.split('=')[0]
        actions = data.split('=')[1]
        # retourne un couple clé, action
        return keys,actions;
                       
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

# Permet de faire appel aux modules    
class workWithModule():
    def __init__(self,module_path,module_name,text):
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
            else:
                notif.update('Erreur',"Vous avez appelez un module sans prononcer le mot de liaison\n"+linker,'ERROR')    
                time.sleep(3)
                notif.close()        
            
        except IOError:
            notif.update('Erreur','Le fichier args du module est absent','ERROR')
            time.sleep(3)
            notif.close()
            sys.exit(1) 
 
# Permet de faire appel aux fonctions basiques
class basicCommands():
    def __init__(self,text):
        # suivant le paramètre reçu, on exécute une action
        if text == 'heure':
            self.getTime()
        elif text == 'batterie':
            self.getPower()
        else:
            print "no action found"
        
    def getTime(self):
        var=time.strftime('%d/%m/%y %H:%M',time.localtime())
        notif.update('Heure',var,'INFO')
            		
    def getPower(self):
        command = "acpi -b"
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output,error  = process.communicate()
        #parsing output
        if output.count('Battery') > 0:
            pcent = output.split(' ')[3]
            rtime = output.split(' ')[4]
            
            if output.count('Charging') > 0:
                message = 'En charge: '+pcent+'\n'+rtime+' avant la fin de la charge'
            else:
                message = 'En décharge: '+pcent+'\n'+rtime+' restant'
        else:
            message = "La batterie n'est pas branchée"
        
        notif.update('Batterie',message,'INFO')
        time.sleep(3)

# Initialisation des notifications
notif = notification('Google2Ubuntu','prêt...')
g2u = interface()
