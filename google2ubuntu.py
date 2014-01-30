#!/usr/bin/env python
# -*- coding: utf-8 -*-
from subprocess import *
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Notify
from os.path import expanduser
import sys
import subprocess 
import os
import json
import urllib2
import urllib
import unicodedata
import time
import gettext
import locale
import re

PID = os.getpid()
lang = locale.getlocale()[0]
gettext.install('google2ubuntu',os.path.dirname(os.path.abspath(__file__))+'/i18n/')

class tts():
    def __init__(self,text):
        text = unicodedata.normalize('NFKD', unicode(text,"utf-8")).encode('ASCII', 'ignore')
        text = text.replace('\n','')
        text_list = re.split('(\,|\.)', text)
        combined_text = []
        output=open('/tmp/tts.mp3',"w")
        lc = lang.split('_')[0]
        
        for idx, val in enumerate(text_list):
            if idx % 2 == 0:
                combined_text.append(val)
            else:
                joined_text = ''.join((combined_text.pop(),val))
                if len(joined_text) < 100:
                    combined_text.append(joined_text)
                else:
                    subparts = re.split('( )', joined_text)
                    temp_string = ""
                    temp_array = []
                    for part in subparts:
                        temp_string = temp_string + part
                        if len(temp_string) > 80:
                            temp_array.append(temp_string)
                            temp_string = ""
                    #append final part
                    temp_array.append(temp_string)
                    combined_text.extend(temp_array)
        #download chunks and write them to the output file
        for idx, val in enumerate(combined_text):
            mp3url = "http://translate.google.com/translate_tts?tl=%s&q=%s&total=%s&idx=%s" % (lc, urllib.quote(val), len(combined_text), idx)
            headers = {"Host":"translate.google.com",
            "Referer":"http://www.gstatic.com/translate/sound_player2.swf",
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.163 Safari/535.19"}
            req = urllib2.Request(mp3url, '', headers)
            sys.stdout.write('.')
            sys.stdout.flush()
            if len(val) > 0:
                try:
                    response = urllib2.urlopen(req)
                    output.write(response.read())
                    time.sleep(.5)
                except urllib2.HTTPError as e:
                    print ('%s' % e)
        output.close()


        os.system("play /tmp/tts.mp3 &")
        



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
        os.system('aplay '+os.path.dirname(os.path.abspath(__file__))+'/sound.wav &')
        notif.update(_('Recording')+':',_('Processing'),'RECORD')
        # On lance le script d'enregistrement pour acquérir la voix pdt 5s
        command =os.path.dirname(os.path.abspath(__file__))+'/record.sh ' + str(PID)
        #p = subprocess.check_call([command])  
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output,error  = p.communicate()
        notif.update(_("End of recording"),_('Sending to Google'),'NETWORK')
        self.sendto()    

    def sendto(self):
        # lecture du fichier audio
        filename='/tmp/voix_'+str(PID)+'.flac'
        f = open(filename)
        data = f.read()
        f.close()
        
        # suppression du fichier audio
        if os.path.isfile('/tmp/voix_'+str(PID)+'.flac'):
            os.system('rm /tmp/voix_'+str(PID)+'.flac')
        
        # envoi d'une requête à Google
        req = urllib2.Request('https://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&lang='+lang, data=data, headers={'Content-type': 'audio/x-flac; rate=16000'})
        try:
            # retour de la requête
            ret = urllib2.urlopen(req)
            try:
                # parsing du retour
                result=json.loads(ret.read())['hypotheses']
                if len(result) != 0:
                    # si on a un résultat
                    text = result[0]['utterance']
                    notif.update(_("Searching action associated to")+':',text,'EXECUTE')
                    
                    # fichier de configuration
                    config = expanduser('~') + '/.config/google2ubuntu/google2ubuntu.conf'
                    default = os.path.dirname(os.path.abspath(__file__))+'/default.conf'
                    if os.path.exists(config):
                        config_file = config
                    else:
                        if os.path.exists(expanduser('~') +'/.config/google2ubuntu') == False:
                            os.makedirs(expanduser('~') +'/.config/google2ubuntu')
                            os.system('cp -r /usr/share/google2ubuntu/modules '+expanduser('~') +'/.config/google2ubuntu')    
                
                        config_file = default
                    
                    # parsing du résultat pour trouver l'action
                    sp = stringParser(text,config_file)
                else:
                    notif.update(_('Error'),_("I don't understand what you are saying"),'ERROR')
                    tts(_('Error')+' '+_("I don't understand what you are saying"))
                    time.sleep(3)
                    notif.close()
                    sys.exit(1)                
                    
            except ValueError, IndexError:
                notif.update(_('Error'),_('Unable to translate'),'ERROR')
                tts(_('Error')+' '+_('Unable to translate'))
                time.sleep(3)
                notif.close()
                sys.exit(1)
                
        except urllib2.URLError:
            notif.update(_('Error'),_('Unable to send to Google'),'ERROR') 
            tts(_('Error')+' '+_('Unable to send to Google'))  
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
                wm = workWithModule(check[2],check[3],text)
            elif _('internal') in check:
                # on execute une commande intene, la commande est configurée
                # ainsi interne/batterie, on envoie batterie à la fonction
                b = basicCommands(check[1])
            else:
                # on exécute directement l'action
                tts(_('Processing'))
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
                
                tts (_('Search results for')+' '+param)
                execute = expanduser('~') +'/.config/google2ubuntu/modules/'+module_path+'/'+module_name+' '+param
                os.system(execute)
            else:
                notif.update(_('Error'),_("you didn't say the linking word")+'\n'+linker,'ERROR')    
                tts(_('Error')+' '+_("you didn't say the linking word"))
                time.sleep(3)
                notif.close()        
            
        except IOError:
            notif.update(_('Error'),_('args file missing'),'ERROR')
            tts(_('Error')+' '+-('args file missing'))
            time.sleep(3)
            notif.close()
            sys.exit(1) 
 
# Permet de faire appel aux fonctions basiques
class basicCommands():
    def __init__(self,text):
        # suivant le paramètre reçu, on exécute une action
        if text == _('time'):
            self.getTime()
        elif text == _('power'):
            self.getPower()
        elif text == _('clipboard'):
            self.read_clipboard()
        else:
            print "no action found"
    
    def read_clipboard(self):
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)

        text = clipboard.wait_for_text()
        if text != None:
            text=text.replace("'",' ')
            print text
            tts(text)
        else:
            tts(_('Nothing in the clipboard'))
    
    def getTime(self):
        var=time.strftime('%d/%m/%y %H:%M',time.localtime())
        notif.update(_('time'),var,'INFO')
            		
    def getPower(self):
        command = "acpi -b"
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output,error  = process.communicate()
        #parsing output
        if output.count('Battery') > 0:
            pcent = output.split(' ')[3]
            rtime = output.split(' ')[4]
            
            if output.count('Charging') > 0:
                message = _('Charging')+': '+pcent+'\n'+rtime+' '+_('before charging')
            else:
                message = _('Discharging')+': '+pcent+'\n'+rtime+' '+_('remaining')
        else:
            message = _('battery is not plugged')
        
        notif.update(_('Power'),message,'INFO')
        tts(message)
        time.sleep(3)

# Initialisation des notifications
notif = notification('Google2Ubuntu',_('Ready'))
g2u = interface()
