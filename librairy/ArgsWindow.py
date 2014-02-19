#!/usr/bin/env python
# -*- coding: utf-8 -*-  
from gi.repository import Gtk
from gi.repository import Notify
from gi.repository import Gdk
from gi.repository import Gio
from os.path import expanduser
import os, sys, subprocess, gettext
import xml.etree.ElementTree as ET

# gère l'apparition de la fenêtre d'assistance de création de module
class ArgsWindow():
    """
    @description: Display a window to help the user create a config for a
    module
    
    @param module
        module's folder
    
    @param name
        module's name
    
    @param store
        a Gtk.Listore in which we will append a new line for this module
    """
    def __init__(self,module,name,store,iter=None):    
        self.grid = Gtk.Grid()
        self.grid.set_border_width(5)
        self.grid.set_row_spacing(5)
        self.grid.set_vexpand(True)
        self.grid.set_hexpand(True)
        self.grid.set_column_spacing(2)
        self.grid.set_column_homogeneous(False)        
        
        label1 = Gtk.Label(_('key sentence'))
        label1.set_justify(Gtk.Justification.LEFT) 
        label1.set_halign(Gtk.Align.START) 
        label1.set_hexpand(True)
        
        label2 = Gtk.Label(_("Linking word"))
        label2.set_justify(Gtk.Justification.LEFT) 
        label2.set_halign(Gtk.Align.START) 

        label3 = Gtk.Label(_("Replace space by plus"))
        label3.set_justify(Gtk.Justification.LEFT) 
        label3.set_halign(Gtk.Align.START) 
        
        ll = Gtk.Label()
        ll.set_vexpand(True)
        
        self.entry1 = Gtk.Entry()
        self.entry1.set_tooltip_text(_('key sentence'))
        
        self.entry2 = Gtk.Entry()
        self.entry2.set_tooltip_text(_("Word to separate call and parameter"))
        self.checkbutton = Gtk.Switch()
        self.checkbutton.set_tooltip_text(_("Replace space by plus"))
        self.checkbutton.set_active(False)
        
        button = Gtk.Button()
        button.set_label(_("Go"))
        button.set_tooltip_text(_("Go"))
        image = Gtk.Image()
        image.set_from_stock(Gtk.STOCK_APPLY, Gtk.IconSize.BUTTON)
        button.set_image(image)
        
        button_cancel = Gtk.Button.new_from_stock(Gtk.STOCK_CANCEL)
        button_cancel.connect("clicked",self.do_destroy)
        
        print module, name
        if iter is None:
            button.connect("clicked",self.do_clicked,module,name,store)
        else:
            self.entry1.set_text(store[iter][0])
            linker = store[iter][3]
            spacebyplus = store[iter][4]
            self.entry2.set_text(linker)
            
            if spacebyplus == '1':
                self.checkbutton.set_active(True)
            button.connect("clicked",self.do_modify,store[iter][3],store,iter)
        
        self.grid.attach(label1,0,0,11,1)
        self.grid.attach(self.entry1,11,0,4,1)        
        self.grid.attach(label2,0,1,11,1)
        self.grid.attach(self.entry2,11,1,4,1)
        self.grid.attach(label3,0,2,14,1)
        self.grid.attach(self.checkbutton,14,2,1,1) 
        self.grid.attach(ll,0,3,15,1)
        self.grid.attach(button_cancel,13,4,1,1)
        self.grid.attach(button,14,4,1,1)    
        self.grid.show_all()            
    
    def do_destroy(self,button):
        self.grid.destroy()    
    
    def get_grid(self):
        return self.grid
        
    def do_clicked(self,button,module,name,store):
        """
        @description: callback function called when the user want to finish
        the configuration of the module. If everything is ok then the config
        file is written at the right place
        """
        key = self.entry1.get_text()
        linker = self.entry2.get_text()
        if self.checkbutton.get_active():
            spacebyplus='1' 
        else:
            spacebyplus='0'
        
        if linker is not '':
            try:
                # folder = name.split('.')[0]
                module_path=expanduser('~')+'/.config/google2ubuntu/modules/'
                                
                os.system('cp '+module+' '+module_path)
                print 'key', key
                print 'name', name
                print 'module', module_path+name
                print 'linker', linker
                print 'spacebyplus', spacebyplus
                store.append([key,name,'modules',linker,spacebyplus])    
                #save the store
                self.saveTree(store)
            except IOError:
                "Unable to open the file"
        
        self.grid.destroy()
    
    def do_modify(self,button,argsfile,store,iter):
        if self.checkbutton.get_active():
           spacebyplus = 1
        else:
           spacebyplus = 0
                
        # modifying the store
        store[iter][0] = self.entry1.get_text()
        store[iter][3] = self.entry2.get_text()
        store[iter][4] = str(spacebyplus)
        
        #save the store
        self.saveTree(store)
        self.grid.destroy()

    def saveTree(self,store):
        """
        @description: save the treeview in the google2ubuntu.xml file
        
        @param: store
            the listStore attach to the treeview
        """
        # if there is still an entry in the model
        config = expanduser('~') +'/.config/google2ubuntu/google2ubuntu.xml'     
        try:
            if not os.path.exists(os.path.dirname(config)):
                os.makedirs(os.path.dirname(config))            
            
            root = ET.Element("data")
            if len(store) != 0:
                for i in range(len(store)):
                    iter = store.get_iter(i)
                    if store[iter][0] != '' and store[iter][1] != '':
                        for s in store[iter][0].split('|'):
                            s = s.lower()
                            s = s.replace('*',' ')
                            Type = ET.SubElement(root, "entry")
                            Type.set("name",unicode(store[iter][2],"utf-8"))
                            Key = ET.SubElement(Type, "key")
                            Key.text = unicode(s,"utf-8")
                            Command = ET.SubElement(Type, "command")
                            Command.text = unicode(store[iter][1],"utf-8")
                            Linker = ET.SubElement(Type, "linker") 
                            Spacebyplus = ET.SubElement(Type, "spacebyplus")
                            if store[iter][3] is not None or store[iter][4] is not None:
                                Linker.text = unicode(store[iter][3],"utf-8")
                                Spacebyplus.text = unicode(store[iter][4],"utf-8")
                
            tree = ET.ElementTree(root).write(config,encoding="utf-8",xml_declaration=True)

        except IOError:
            print "Unable to write the file"   
