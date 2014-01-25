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

class notification():
    def __init__(self,titre,corps):
        Notify.init(titre)
        self.n = Notify.Notification.new(titre,corps,"")
        self.n.set_urgency(Notify.Urgency.CRITICAL)    
        self.n.set_icon_from_pixbuf(Gtk.Label().render_icon(Gtk.STOCK_MEDIA_PLAY, Gtk.IconSize.DIALOG))
        self.n.show()
        time.sleep(0.5)

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
    
    def close(self):
        self.n.close()

# La classe interface permet de lancer l'enregistrement et de communiquer
# avec Google
class interface():
    def __init__(self):
        notif.update('Enregistrement:','En cours','RECORD')
        command =os.path.dirname(os.path.abspath(__file__))+'/record.sh'
        p = subprocess.check_call([command])  
        notif.update("Fin de l'enregistrement",'Envoi à Google','NETWORK')
        self.sendto()    

    def sendto(self):
        filename='/tmp/voix.flac'
        f = open(filename)
        data = f.read()
        f.close()
        req = urllib2.Request('https://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&lang=fr-FR', data=data, headers={'Content-type': 'audio/x-flac; rate=16000'})
        try:
            ret = urllib2.urlopen(req)
            try:
                result=json.loads(ret.read())['hypotheses']
                if len(result) != 0:
                    text = result[0]['utterance']
                    notif.update("Recherche de l'action associee à:",text,'EXECUTE')
                    config = expanduser('~') + '/.config/google2ubuntu/google2ubuntu.conf'
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
            f=open(file,"r")
            max = 0;
            keys=[]
            actions=[]
            do = ''
            cpt=0;
            for ligne in f:
                k,a = self.getKeyAction(ligne)
                keys.extend([k])
                actions.extend([a])        
            
            f.close();
            for i in range(len(keys)):
                tab = self.getAllKeys(keys[i])
                score = 0;
                for j in range(len(tab)):
                    score += text.count(unicode(tab[j],"utf-8"))
                        
                if max < score:
                    max = score
                    do = actions[i]
            
            # on regarde si la commande fait appel à un module
            # si oui, alors on lui passe en paramètre le dernier mot prononcé
            check = do.split('/')
            if check[0] != 'interne': 
                if len(check) >= 4 and check[1] == 'modules':
                        wm = workWithModule(check[2],check[3],text)
                else:
                    os.system(do)
            else:
                b = basicCommands(check[1])
            
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
        return keys,actions;
                       
    def getAllKeys(self,key):
        #extraction des mots
        tab = []
        # get all words
        key = key.strip('*')
        Key = key.split('*')
        for var in Key:
            # get the end of the word
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
            argsfile=expanduser('~')+'/.config/google2ubuntu/modules/'+module_path+'/args';
            print argsfile
            f = open(argsfile,'r')
            ligne=(f.readline()).rstrip('\n\r')  
            linker=unicode(ligne.split('=')[1],"utf-8")
            ligne=(f.readline()).rstrip('\n\r')              
            plus=ligne.split('=')[1] 
            f.close()  

            if text.count(linker) > 0:
                param = text.split(linker)[1]
                                   
                if plus == 1:
                    param=param.replace(' ','+')
                print "ok go"
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
