# -*- coding: utf-8 -*-  
#!/usr/bin/env python
from subprocess import *
import sys
import gtk
import subprocess 
import os
import json
import urllib2
import pynotify
import time

pynotify.init("Google2Ubuntu")
n = pynotify.Notification("Google2Ubuntu est pret","")
n.set_urgency(pynotify.URGENCY_CRITICAL)    
n.set_icon_from_pixbuf(gtk.Label().render_icon(gtk.STOCK_MEDIA_PLAY, gtk.ICON_SIZE_DIALOG))
n.show()

class interface():
    def __init__(self):
        n.update("Enregistrememnt:","En cours...")
        n.set_icon_from_pixbuf(gtk.Label().render_icon(gtk.STOCK_MEDIA_RECORD, gtk.ICON_SIZE_DIALOG))
        n.show()
        p = subprocess.check_call(['./record.sh'])  
        n.update("Fin de l'enregistrement !","Envoi a Google")
        n.set_icon_from_pixbuf(gtk.Label().render_icon(gtk.STOCK_NETWORK, gtk.ICON_SIZE_DIALOG))
        n.show()
        self.sendto()    

    def sendto(self):
        filename='voix.flac'
        f = open(filename)
        data = f.read()
        f.close()
        req = urllib2.Request('https://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&lang=fr-FR', data=data, headers={'Content-type': 'audio/x-flac; rate=16000'})
        try:
            ret = urllib2.urlopen(req)
            try:
                text = json.loads(ret.read())['hypotheses'][0]['utterance']
                n.update("Recherche de l'action associée a ",text)
                n.set_icon_from_pixbuf(gtk.Label().render_icon(gtk.STOCK_EXECUTE, gtk.ICON_SIZE_DIALOG))
                n.show()
                sp = stringParser(text,os.getcwd()+'/google2ubuntu.conf')
            except ValueError:
                n.update("Erreur:","Traduction Impossible")
                n.set_icon_from_pixbuf(gtk.Label().render_icon(gtk.STOCK_DIALOG_ERROR, gtk.ICON_SIZE_DIALOG))
                n.show()
                time.sleep(3)
                n.close()
                sys.exit(1)
        except urllib2.URLError:
            n.update("Erreur:","Envoi à Google impossible")
            n.set_icon_from_pixbuf(gtk.Label().render_icon(gtk.STOCK_DIALOG_ERROR, gtk.ICON_SIZE_DIALOG))
            n.show()
            time.sleep(3)
            n.close()
            sys.exit(1)

            
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
                    score += text.count(tab[j])
                        
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
            n.close()
            
        except IOError:
            n.update("Erreur:","Lecture fichier config impossible")
            n.set_icon_from_pixbuf(gtk.Label().render_icon(gtk.STOCK_DIALOG_ERROR, gtk.ICON_SIZE_DIALOG))
            n.show()
            time.sleep(3)
            n.close()            
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
        key = key.rstrip('*')
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
    
class workWithModule():
    def __init__(self,module_path,module_name,text):
        try:
            argsfile='modules/'+module_path+'/args';
            print argsfile
            f = open(argsfile,'r')
            ligne=(f.readline()).rstrip('\n\r')  
            linker=ligne.split('=')[1]
            ligne=(f.readline()).rstrip('\n\r')              
            plus=ligne.split('=')[1] 
            f.close()  
            
            print text.split(linker)
            if text.count(linker) > 0:
                param = text.split(linker)[1]
                                   
                if plus == 1:
                    param=param.replace(' ','+')
        
                os.system('./modules/'+module_path+'/'+module_name+' '+param)
            else:
                n.update("Erreur:","Vous avez appelez un module sans prononcer le mot de liaison\n"+linker)
                n.set_icon_from_pixbuf(gtk.Label().render_icon(gtk.STOCK_DIALOG_ERROR, gtk.ICON_SIZE_DIALOG))
                n.show()
                time.sleep(3)
                n.close()                
            
        except IOError:
            n.update("Erreur:","Le fichier args associé au module est absent ou illisible")
            n.set_icon_from_pixbuf(gtk.Label().render_icon(gtk.STOCK_DIALOG_ERROR, gtk.ICON_SIZE_DIALOG))
            n.show()
            time.sleep(3)
            n.close()
            sys.exit(1) 
            
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
        n.update("Système",var)
        n.set_icon_from_pixbuf(gtk.Label().render_icon(gtk.STOCK_YES, gtk.ICON_SIZE_DIALOG))
        n.show()
            		
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
                message = 'En déchage: '+pcent+'\n'+rtime+' restant'
        else:
            message = "La batterie n'est pas branchée"
        
        n.update("Batterie",message)
        n.set_icon_from_pixbuf(gtk.Label().render_icon(gtk.STOCK_DIALOG_INFO, gtk.ICON_SIZE_DIALOG))
        n.show()
        time.sleep(3)

g2u = interface()
